export class Repo<T extends { id: string }> {
  constructor(private data: T[]) {}

  public get(id: string): T | undefined {
    return this.data.find((item) => item.id === id);
  }

  public getAll(): T[] {
    return [...this.data];
  }

  public size(): number {
    return this.data.length;
  }
}
