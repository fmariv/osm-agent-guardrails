# Security and responsible infrastructure usage

Do not disclose personal or access data in issues, PRs or test fixtures. Never submit real API keys, user credentials, server logs with identifiable clients, or bulk OSM data snapshots here.

This repository contains example clients, not security-hardened production services. Review proxy behavior, SSRF controls, URL validation, caching semantics, logging and rate limiting before reuse. No example should be promoted as a universal limiter protecting public OSM services.

Report a security issue privately to the repository maintainer through GitHub private vulnerability reporting if enabled; otherwise contact the owner directly, without public exploit details.
