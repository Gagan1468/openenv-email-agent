# OpenEnv Email Agent

## Overview
This environment simulates AI email routing in a customer support system.

## Tasks
- easy: basic classification
- medium: varied phrasing
- hard: ambiguous emails
- expert: noisy classification

## Reward
Continuous reward (0.05–0.95) based on:
- correctness
- task difficulty
- stochastic realism

## Agent
LLM-based classifier via LiteLLM proxy.

## Determinism
Environment seeded for reproducible evaluation.
