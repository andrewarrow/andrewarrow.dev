It is time to become a tech prepper

<div style="max-width: 100%; margin: 2rem auto;">
  <img src="/assets/images/cloud.jpeg" alt="Cloud infrastructure" style="width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
</div>

Today made it obvious again. Big clouds can wobble. Entire regions can stall. Trust alone is not a strategy. If you run software that people pay for or rely on, you must assume that any part of your stack can vanish at any moment. The only honest response is to engineer for constant failure and instant recovery. That means building on three pillars at the same time. Bare metal you control. Amazon Web Services. A second non Amazon cloud. Any one of the three can become the primary at any moment. Any one can be dark while the other two carry the load within seconds.

Here is a practical playbook for that world. Each point is written with seconds in mind, not hours.

1. Treat bare metal as a first class home for your entire company
   Bare metal is not a sidecar for short term emergencies. It is a full runway. Pick two unrelated providers in different regions. Stand up identical clusters with the same container runtime and the same service mesh you use in the clouds. Keep capacity warm with low cost background jobs so that autoscaling has headroom. Your goal is to move the entire operation there when a cloud is dark, not a few background workers. Practice real switchovers with traffic.

2. Run a tri cloud control plane that never sleeps
   Put a small always on control plane in each pillar. One in bare metal. One in Amazon. One in your second cloud. Use Git Ops so that desired state lives outside any single provider. A change to main is the source of truth. Agents in all three pillars reconcile from the same repo and the same secret store. If a pillar goes dark, the other two keep reconciling.

3. Make the app stateless by default and explicit where state lives
   Everything that can be stateless should be stateless. Session data goes to an external store with global replication. Media goes to object storage that is mirrored across providers. Only a small set of services are allowed to keep state. Those services have deep, explicit runbooks and replication topologies.

4. Design a portable data layer with two paths to truth
   Choose a primary database engine that runs well on all three pillars. Postgres is the common choice. Use logical replication across pillars with change data capture so you can promote in seconds. For document or key value workloads, use a store that has native multi region features in the cloud but that can also run on bare metal. When you are in Amazon, you may use a managed service, but you still stream changes into your portable engine. That way a promotion outside Amazon is not a cold start. You always have two paths to truth.

5. Adopt active active traffic from day one
   Users should already be hitting at least two pillars before any outage. Use global anycast through multiple providers to get traffic to the closest healthy edge. Health checks must live outside any single pillar. When one pillar fails a check, traffic drains in seconds without human hands. No late night DNS edits. No email threads. It just fails away.

6. Keep identity alive even when your main provider sleeps
   Most outages turn nasty when nobody can log in. Mirror your identity provider. Sync users and keys in near real time. Build an emergency mode that allows scoped service accounts to act with time boxed tokens issued by a separate signer that runs in all three pillars. Your team must be able to reach dashboards and deploys when one SSO vendor is dark.

7. Package everything once and run it everywhere
   Build a single container image per service. Publish to at least two registries, one inside Amazon and one outside. Mirror tags to a private registry that runs on bare metal. At deploy time, clusters pull from the nearest healthy registry with a signed policy. A registry outage does not block a rollout.

8. Push logs and metrics to a dual home brain
   Observability dies first during a big outage. Run collectors in each pillar that ship to two separate back ends. One can be managed in a cloud. One must be self hosted on bare metal or a second vendor. The same holds for alerts. Pager and chat must have a fallback. If your only alert path depends on the cloud that is down, you are flying blind.

9. Practice fast promotions like a racing pit crew
   Write down the exact steps to promote a standby database, a cache tier, or an object storage mirror. Automate most of it, but still run the drill monthly. Record times. Remove steps. Your goal is a clean promotion in under two minutes for each stateful layer. Make it sport. Reward the team when they beat last month.

10. Offer graceful degradation that users actually appreciate
    Build a reduced feature mode that keeps the core promise of your product when parts of the stack are dark. Read only views. Local drafts. Queued actions that sync later. Clear status banners. A user who can still do the essential job will forgive a lot. A blank spinner earns rage and churn.

<div style="max-width: 100%; margin: 2rem auto;">
  <img src="/assets/images/cloud2.jpeg" alt="Multi-cloud architecture" style="width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
</div>

How the pieces click in seconds

A user hits your domain. Anycast routes to the closest edge from two providers at once. The edge checks health for three origins, one in each pillar. Amazon fails a probe. The edge shifts weight to the second cloud and bare metal. Requests land on stateless app pods. Sessions resolve from the shared store that is already multi region. The app reads from Postgres that has a hot follower in both surviving pillars. A tiny controller promotes the follower in the second cloud because latency is best for the majority of traffic right now. Replication resumes from there to bare metal. Writes flow. The user keeps working.

Your team gets alerts through two channels. The deploy system stays up because the control plane lives in all three pillars. A small patch ships. The edge config receives it within a minute because config is in Git, not in a single vendor console.

Contracts and costs that make this real

This plan sounds pricey. It is not free. It is also cheaper than days of downtime and the brand damage that follows. To keep costs under control, reserve steady capacity in one pillar. Keep warm but not hot capacity in the other two. Use savings plans or committed use where it makes sense, but never lock into a single pillar for core pieces. Negotiate burst pools with bare metal providers. Use spot or preemptible nodes for non critical workers in the standby pillars so the meter stays low while readiness stays high.

Culture that survives outages

Resilience is not only technology. It is a habit. Treat failure like a daily event. Hold five minute game days where someone kills a dependency and the team watches the system heal. Write short postmortems with clear next steps. Celebrate clean failovers the same way you celebrate a big feature launch. The team will take the hint and keep building with resilience in mind.

A simple checklist to start this week

Pick a second cloud and a bare metal provider. Stand up a tiny replica of your stack in both. Wire global traffic across all three pillars for a single low risk service. Mirror its data. Prove that you can kill the service in Amazon and keep user traffic flowing within seconds. Expand from there, service by service, database by database. Make the drills routine.

<div style="max-width: 100%; margin: 2rem auto;">
  <img src="../../../assets/images/world.jpeg" alt="Global infrastructure" style="width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
</div>

The future is messy. Big vendors will keep having bad days. Routers will misbehave. Power will fail. Your users will not care why. They will care that your product keeps working. Build for that reality now. Become a tech prepper with three sturdy pillars under your feet. When the next outage hits, your lights stay on.

