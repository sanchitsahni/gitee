+++
title = "gitee"
chapter = false
weight = 5
+++

## Table of Contents

1. [Overview](#overview)
2. [Setup](#setup)
3. [Agent Build](#agent-build)
4. [OPSEC](#opsec)

## Overview

The Gitee C2 profile enables command and control communication through Gitee issue comments and file operations. Setup requires:

- Gitee repository (private recommended)
- Two issues for bidirectional messaging
- Webhook configuration for event notifications
- Personal Access Token for API authentication

## Setup

### 1. Create Gitee Repository

1. Navigate to gitee.com and create a new private repository
2. Add a README file to initialize the repository
3. Enable the main branch creation

### 2. Create Issues

Create two issues in your repository:
- Issue #1: For Mythic server commands
- Issue #2: For agent responses

Navigate to `https://gitee.com/$USER/$REPO/issues` and create these issues.

### 3. Configure Webhook

1. Go to repository settings at `https://gitee.com/$USER/$REPO/hooks`
2. Add webhook with these settings:
   - **Payload URL**: `http://<mythic-server>:<port>/`
   - **Content Type**: application/json
   - **Secret**: Any secure string (save for configuration)
   - **Events**: Send all events
   - **SSL Verification**: Disable
   - **Active**: Enabled

### 4. Generate Personal Access Token

1. Go to Gitee Settings → Security → Personal Access Tokens
2. Generate new token with:
   - **Expiration**: Appropriate for operation duration
   - **Repository Access**: Select your C2 repository
   - **Permissions**:
     - Contents: Read and Write
     - Issues: Read and Write
3. Copy token (starts with xxxxx)

### 5. Mythic Configuration

Configure the C2 profile with:

```json
{
    "owner": "username",
    "repo": "repository_name",
    "server_issue": 1,
    "client_issue": 2,
    "gitee_token": "xxxxxxxxxx",
    "webhook_secret": "your_secret",
    "port": "1234"
}
```

## Agent Build

### Profile Parameters

- **Callback Interval**: Time between agent requests (seconds)
- **Callback Jitter**: Randomization percentage
- **Crypto Type**: aes256_hmac or none
- **Kill Date**: Agent expiration date
- **User Agent**: Custom HTTP user agent
- **Proxy Settings**: Optional proxy configuration

## OPSEC

Security considerations:

- Keep repository private
- Use strong webhook secrets
- Rotate access tokens regularly
- Monitor webhook logs
- Use HTTPS where possible
- Restrict token permissions to minimum required
