
# Google Cloud SDK Commands

This document provides a list of some common Google Cloud SDK commands.

## Contents

- [Google Cloud SDK Commands](#google-cloud-sdk-commands)
  - [Contents](#contents)
  - [Current Active User](#current-active-user)
  - [Current Active Project](#current-active-project)
  - [Switch to Different Project](#switch-to-different-project)
  - [FAQ](#faq)

## Current Active User

To see the current active user, use the following command:

```bash
gcloud auth list
```

## Current Active Project
To see the current active project, use the following command:

```bash
gcloud config get-value project
```

## Switch to Different Project
To switch to a different Google Cloud project, use the following command (replace PROJECT_ID with your project's ID):

```bash
gcloud config set project PROJECT_ID
```

## FAQ

1.  The error message indicates that the current authenticated user does not have the necessary permissions (bigquery.jobs.create) to create jobs in the project random-stuff-389717

