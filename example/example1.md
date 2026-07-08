# `time` package in Go

Here are some commonly used functions and types from Go's `time` package:

## Getting the current time

```go
now := time.Now()
```

## Parsing and formatting

Go uses a reference date (`Mon Jan 2 15:04:05 MST 2006`) instead of format verbs like `%Y-%m-%d`.

```go
t, err := time.Parse("2006-01-02", "2026-07-05")
formatted := t.Format("2006-01-02 15:04:05")
```
