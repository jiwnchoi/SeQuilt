// types.ts
export type Subscriber<T> = (state: T) => void

// store.ts
export class Store<T> {
  private state: T
  private subscribers: Set<Subscriber<T>> = new Set()

  constructor(initialState: T) {
    this.state = initialState
  }

  getState(): T {
    return this.state
  }

  setState(newState: T): void {
    this.state = newState
    this.notify()
  }

  subscribe(subscriber: Subscriber<T>): () => void {
    this.subscribers.add(subscriber)
    return () => this.unsubscribe(subscriber)
  }

  unsubscribe(subscriber: Subscriber<T>): void {
    this.subscribers.delete(subscriber)
  }

  private notify(): void {
    for (const subscriber of this.subscribers) {
      subscriber(this.state)
    }
  }
}

// subscription.ts
export class Subscription<T> {
  private store: Store<T>
  private subscriber: Subscriber<T>
  private isActive: boolean = false

  constructor(store: Store<T>, subscriber: Subscriber<T>) {
    this.store = store
    this.subscriber = subscriber
  }

  subscribe(): void {
    if (!this.isActive) {
      this.store.subscribe(this.subscriber)
      this.isActive = true
    }
  }

  unsubscribe(): void {
    if (this.isActive) {
      this.store.unsubscribe(this.subscriber)
      this.isActive = false
    }
  }

  isSubscribed(): boolean {
    return this.isActive
  }
}
