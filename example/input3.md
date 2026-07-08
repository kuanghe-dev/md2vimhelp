**Key points:**
- Always pass the `WaitGroup` by pointer (`*sync.WaitGroup`), otherwise each goroutine gets its own copy of the counter.
- Call `Add()` *before* starting the goroutine, not inside it — otherwise `Wait()` might return before all `Add()` calls happen (race condition).
- Use `defer wg.Done()` at the top of the goroutine so it runs even if the function panics or returns early.

## Common Pitfalls

1. **Copying a WaitGroup** — since it contains internal state, copying it (e.g., passing by value into a function) breaks it. Always use a pointer.
2. **Calling `Add` after `Wait` has already been called and reached zero** — this causes a race condition; `Add` calls should happen before or concurrently with, never logically "after," the matching `Wait`.
3. **Mismatched `Add`/`Done` counts** — if `Done()` is called more times than `Add()`, you'll get a panic: `sync: negative WaitGroup counter`. If fewer, `Wait()` blocks forever (deadlock).
4. **Forgetting `defer`** — if the goroutine panics before reaching a non-deferred `Done()` call, the counter never decrements, causing `Wait()` to hang forever.

Would you like an example combining `WaitGroup` with a mutex (e.g., safely incrementing a shared counter across goroutines)?
