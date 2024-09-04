# Manufacturing Workloads

This repository contains a set of workloads designed for analyzing and optimizing various aspects of manufacturing processes. Each workload performs specific tasks such as object detection, safety gear compliance, time-in-zone analysis, and object frequency and distribution.

## Workloads Overview

Below is an overview of the available workloads:

### 1. Workload presented during midterm review
- **Directory**: [`workload_test`](workloads/workload_test)
- **Purpose**:

### 2. **Object Frequency and Distribution Analysis**
- **Directory**: [`workload_object_distribution`](https://github.com/your-repo/workloads/workload_object_distribution)
- **Purpose**: Understand the frequency and distribution of detected objects across different areas on the floor.
- **Key Insights**:
	- Identify commonly detected objects (e.g., tools, machines, vehicles) to track the availability and utilization of assets.
	- Detect potential misplacement of items (e.g., safety equipment like helmets or gloves in the wrong areas).
- **Metrics**:
	- Frequency of object detections per area or zone.
	- Most and least commonly detected objects.
	- Distribution of high-priority objects (e.g., safety gear, medical equipment).

### 3. **Operational Efficiency Analysis**
- **Directory**: [`workload_operational_efficiency`](https://github.com/your-repo/workloads/workload_operational_efficiency)
- **Purpose**: Measure the operational efficiency by tracking object movements and analyzing workflows.
- **Key Insights**:
	- Monitor the flow of items like carts, vehicles, and materials across the manufacturing floor to detect inefficiencies or bottlenecks.
	- Analyze how frequently tools are used and how efficiently they are returned to their designated areas.
	- Track the movement of materials (e.g., containers, boxes) to ensure they follow the correct workflow.
- **Metrics**:
	- Time taken for items (e.g., carts, boxes) to move through the manufacturing process.
	- Frequency of item transfers between zones.
	- Average time for tools to be used and returned to storage.

### 4. **Anomaly Detection**
- **Directory**: [`workload_anomaly_detection`](https://github.com/your-repo/workloads/workload_anomaly_detection)
- **Purpose**: Detect unusual patterns that could indicate operational issues, safety risks, or process deviations.
- **Key Insights**:
	- Identify out-of-place objects, such as a ladder in a restricted zone or a vehicle in a non-vehicle area.
	- Detect anomalies in object usage patterns (e.g., overuse or underuse of specific tools).
	- Monitor for objects that are misplaced or not being used according to protocol (e.g., medical equipment in the wrong area).
- **Metrics**:
	- Anomaly detection rate for misplaced items.
	- Detection of unusual object frequencies in specific areas.
	- Frequency of out-of-place objects or items detected in restricted zones.

### 5. **Human-Object Interaction Analysis**
- **Directory**: [`workload_human_object_interaction`](https://github.com/your-repo/workloads/workload_human_object_interaction)
- **Purpose**: Analyze interactions between workers and detected objects to improve efficiency, safety, and ergonomics.
- **Key Insights**:
	- Track the use of tools and machinery by workers to ensure proper handling and safety.
	- Analyze the frequency of interactions between humans and objects like tools, vehicles, and appliances.
	- Detect unsafe interactions, such as humans too close to dangerous equipment (e.g., chainsaws, drills).
- **Metrics**:
	- Worker interaction frequency with key tools and equipment.
	- Proximity analysis between humans and potentially dangerous objects.
	- Safety compliance based on worker-object interactions (e.g., wearing safety gloves when handling certain tools).
