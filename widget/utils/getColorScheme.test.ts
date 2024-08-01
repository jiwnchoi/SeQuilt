import { hsl, schemeCategory10 } from "d3";
import getColorScheme from "./getColorScheme";

describe("getColorScheme", () => {
  it("should return an array of colors", () => {
    const result = getColorScheme(5);
    expect(Array.isArray(result)).toBe(true);
    expect(result.length).toBe(5);
  });

  it("should return the correct number of colors", () => {
    expect(getColorScheme(3).length).toBe(3);
    expect(getColorScheme(10).length).toBe(10);
    expect(getColorScheme(20).length).toBe(20);
  });

  it("should return original schemeCategory10 colors for size <= 10", () => {
    const result = getColorScheme(10);
    expect(result).toEqual(schemeCategory10);
  });

  it("should include lighter colors after the first 10", () => {
    const result = getColorScheme(15);
    const lighterColor = hsl(schemeCategory10[0]).brighter().toString();
    expect(result).toContain(lighterColor);
  });

  it("should include darker colors after the first 20", () => {
    const result = getColorScheme(25);
    const darkerColor = hsl(schemeCategory10[0]).darker().toString();
    expect(result).toContain(darkerColor);
  });

  it("should return all available colors if size is greater than extended scheme", () => {
    const result = getColorScheme(100);
    expect(result.length).toBe(schemeCategory10.length * 3);
  });

  it("should return an empty array if size is 0", () => {
    const result = getColorScheme(0);
    expect(result).toEqual([]);
  });

  it("should handle negative sizes by returning an empty array", () => {
    const result = getColorScheme(-5);
    expect(result).toEqual([]);
  });
});
