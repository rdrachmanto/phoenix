## Phoenix

Pi-based task runner with degradation targeting battery-free deployments (currently on solar panel and 2x10F supercapacitors)

## Baseline List

| Name      | Behavior                                                                                  |
|-----------|-------------------------------------------------------------------------------------------|
| QueueOnly | if there's something in the queue, always do that instead of starting new                 |
| Atomic    | Always start new instead of doing something from the queue                                |
| CatNap    | Degrade based on programmer-set threshold                                                 |
| Quetzal   | Predictive degradation based on Little's Law, degrade earlier before overflow is imminent |
