# TTL Triage - Carlos Configuration Error Reproduction

This repository reproduces Carlos's TTL configuration issue that causes the `Configuration.__init__()` error in LangGraph Platform.

## Issue Description

Carlos reported that applying assistant-level TTL configuration causes this error:
```
Configuration.__init__() got an unexpected keyword argument 'host'
```

## Setup

This repo contains Carlos's **exact configuration**:

### langgraph.json
- **TTL settings**: 1-minute expiration, 1-minute sweep intervals (Carlos's tested config)
- **Graphs**: `support_agent_flow` and `ai_poi_extraction`
- **Paths**: Exact same as Carlos's setup

### Agents
- `src/digitt_agentflow/graph.py` - Simple support agent
- `src/ai_poi_extraction/graph.py` - Simple extraction agent

## Test Scripts

- `create_assistants_and_test.py` - Creates assistants and applies Carlos's TTL config
- `reproduce_carlos_error.py` - Focused reproduction of the Configuration error

## How to Reproduce

1. Deploy this to LangGraph Platform Cloud (not local dev)
2. Run the test scripts
3. Look for the `Configuration.__init__()` error when applying assistant-level TTL config

## Carlos's Configuration That Causes Error

```python
assistant = await client.assistants.update(
    assistant_id=ai_poi_extraction_assistant_id,
    config={
        "checkpointer": {
            "ttl": {
                "strategy": "delete",
                "sweep_interval_minutes": 60,
                "default_ttl": 10080
            }
        },
        "store": {
            "ttl": {
                "refresh_on_read": True,
                "sweep_interval_minutes": 120,
                "default_ttl": 10080
            }
        }
    }
)
```

The error occurs during `client.runs.join()` after applying this TTL configuration.