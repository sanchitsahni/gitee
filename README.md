# Gitee C2 Profile

A [Mythic](https://github.com/its-a-feature/Mythic) C2 Profile that enables command and control communication via Gitee issue comments and file operations.

## Overview

This C2 profile leverages Gitee as a communication channel for agent and server interactions. It supports bidirectional communication through issue comments and repository file operations, providing a covert and reliable command & control infrastructure.

## Installation

To install this C2 profile on your Mythic server, execute:

```bash
sudo ./mythic-cli install gitee https://github.com/MythicC2Profiles/gitee
```

## Quick Start

1. Create a Gitee repository for C2 communications
2. Set up two issues (one for server commands, one for agent responses)
3. Configure webhook notifications to your Mythic server
4. Generate a Gitee personal access token
5. Deploy the profile and configure agents

## Key Features

- **Issue-based Communication**: Commands and responses flow through Gitee issues
- **File-based Tasking**: Large data transfers via repository files
- **Webhook Integration**: Automatic notifications on repository events
- **Token Authentication**: Secure API access using personal access tokens
- **Bidirectional C2**: Full command and control capabilities

## Compatible Agents

- Athena

## Project Structure

```
gitee/
├── README.md
├── LICENSE
├── config.json
├── C2_Profiles/gitee/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── gitee/
│       ├── c2_code/
│       │   ├── config.py
│       │   ├── config.json
│       │   ├── gitee_client.py
│       │   ├── mythic_client.py
│       │   └── server.py
│       └── c2_functions/
│           └── gitee.py
├── documentation-c2/gitee/
│   └── _index.md
└── agent_icons/
```

## Setup Guide

### 1. Prepare Gitee Repository

- Create a private Gitee repository
- Create Issue #1 for server commands
- Create Issue #2 for agent responses
- Note the repository owner and name

### 2. Generate Access Token

1. Log in to Gitee
2. Navigate to Settings → Security Settings → Personal Access Tokens
3. Generate a token with repository read/write access
4. Keep the token secure

### 3. Configure Webhook

1. Go to repository Settings → Webhooks
2. Set webhook URL to: `https://<mythic-server>:port/`
3. Select "Push" and "Issue Comment" events
4. Set webhook secret
5. Enable SSL verification

## Development

The C2 profile is implemented in Python:

- **config.py**: Configuration management
- **gitee_client.py**: Gitee API interactions
- **mythic_client.py**: Mythic server communication
- **server.py**: Webhook receiver
- **gitee.py**: C2 profile definition

## Dependencies

- aiohttp
- quart
- mythic_container

## Security Considerations

- Use private repositories
- Rotate tokens regularly
- Enable webhook signature verification
- Use HTTPS for all communications
- Restrict token permissions

## License

See LICENSE file.
