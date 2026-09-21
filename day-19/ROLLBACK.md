# Rollback Guide

## Identify current branch

git branch

## Identify recent commits

git log --oneline -10

## Inspect commit

git show <commit>

## Safe rollback strategy

Create a rollback branch before reverting.

git checkout -b rollback-day19

## Revert a bad commit

git revert <commit-sha>

## Verify

pytest -v

## Push

git push origin rollback-day19