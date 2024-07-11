def extract_run_data(pipeline_names, adf_client, common_filter_params):
    run_data = []
    for row in pipeline_names.collect():
        pipeline_name = row.PipelineName
        try:
            runs = get_pipeline_runs(adf_client, pipeline_name, common_filter_params)
            latest_run = get_latest_run(runs)
            if latest_run:
                est_start = convert_to_est(latest_run.run_start)
                est_end = convert_to_est(latest_run.run_end)

                # Extract failed activities and their timestamps
                activities_response = adf_client.activity_runs.query_by_pipeline_run('rg', 'factory', pipeline_name, latest_run.run_id)
                activities = activities_response.value

                failed_activities_info = [
                    (activity.activity_name, activity.status, activity.activity_run_start)
                    for activity in activities if activity.status == 'Failed'
                ]

                activity_names = []
                failed_times = []

                for activity_name, status, failed_time in failed_activities_info:
                    if 'Failure' not in activity_name:
                        activity_names.append(activity_name)
                        failed_times.append(failed_time)

                if len(activity_names) > 1:
                    formatted_activity_names = '|'.join(activity_names)
                    formatted_failed_times = '|'.join(map(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'), failed_times))
                else:
                    formatted_activity_names = activity_names[0] if activity_names else ''
                    formatted_failed_times = failed_times[0].strftime('%Y-%m-%d %H:%M:%S') if failed_times else ''

                run_data.append((
                    pipeline_name,
                    latest_run.run_id,
                    latest_run.status,
                    est_start,
                    est_end,
                    formatted_activity_names,  # CurrentFailure
                    formatted_failed_times     # CurrentFailureTimeStamp
                ))
                print(f"Run data for {pipeline_name}: Start - {est_start}, End - {est_end}, Failure - {formatted_activity_names}, Failure Time - {formatted_failed_times}")
        except Exception as e:
            displayHTML(f"<p style='color:red;'>Failed to get pipeline runs for {pipeline_name}: {e}</p>")
    return run_data



def update_child_delta_table(spark, child_delta_table_path, run_data):
    if run_data:
        # Create schema with all fields as StringType initially
        schema = StructType([
            StructField("PipelineName", StringType(), True),
            StructField("LatestRunID", StringType(), True),
            StructField("LatestRunStatus", StringType(), True),
            StructField("LatestRunStartTime", StringType(), True),  # Initially as StringType
            StructField("LatestRunEndTime", StringType(), True),    # Initially as StringType
            StructField("CurrentFailure", StringType(), True),
            StructField("CurrentFailureTimeStamp", StringType(), True),
            StructField("AllFailures", StringType(), True),
            StructField("AllFailuresTimeStamp", StringType(), True)
        ])
        
        run_df = spark.createDataFrame(run_data, schema)
        
        # Convert the string timestamps back to TimestampType
        run_df = run_df.withColumn("LatestRunStartTime", to_timestamp("LatestRunStartTime", "yyyy-MM-dd'T'HH:mm:ss.SSS"))
        run_df = run_df.withColumn("LatestRunEndTime", to_timestamp("LatestRunEndTime", "yyyy-MM-dd'T'HH:mm:ss.SSS"))

        distinct_run_df = run_df.distinct()

        delta_table_child = DeltaTable.forPath(spark, child_delta_table_path)
        delta_table_child.alias("existingData").merge(
            distinct_run_df.alias("newData"),
            "existingData.PipelineName = newData.PipelineName AND existingData.IsActive = 1"
        ).whenMatchedUpdate(set={
            "LatestRunID": "newData.LatestRunID",
            "LatestRunStatus": "newData.LatestRunStatus",
            "LatestRunStartTime": "newData.LatestRunStartTime",
            "LatestRunEndTime": "newData.LatestRunEndTime",
            "CurrentFailure": "newData.CurrentFailure",
            "CurrentFailureTimeStamp": "CAST(newData.CurrentFailureTimeStamp AS STRING)",
            "AllFailures": "CASE WHEN newData.CurrentFailure <> '' THEN " +
                           "CASE WHEN coalesce(existingData.AllFailures, '') = '' THEN newData.CurrentFailure " +
                           "ELSE concat(existingData.AllFailures, ' | ', newData.CurrentFailure) END " +
                           "ELSE existingData.AllFailures END",
            "AllFailuresTimeStamp": "CASE WHEN newData.CurrentFailureTimeStamp IS NOT NULL THEN " +
                                     "CASE WHEN coalesce(existingData.AllFailuresTimeStamp, '') = '' THEN CAST(newData.CurrentFailureTimeStamp AS STRING) " +
                                     "ELSE concat(existingData.AllFailuresTimeStamp, ' | ', CAST(newData.CurrentFailureTimeStamp AS STRING)) END " +
                                     "ELSE existingData.AllFailuresTimeStamp END"
        }).execute()
        
        displayHTML("<p style='color:green;'>Child Delta table updated successfully.</p>")
        print("Child Delta table updated successfully.")
    else:
        displayHTML("<p style='color:orange;'>No data available to update the Child Delta table.</p>")
        print("No data available to update the Child Delta table.")
