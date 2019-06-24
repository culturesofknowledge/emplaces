import { Facet } from "./Facet";

export class SearchResult {
  facets: Facet[];
  results: ResultItem[];
  total: number;
  constructor(total: number, data: ResultItem[], facets: Facet[]) {
    this.total = total;
    this.results = data;
    this.facets = facets;
  }
}

export class ResultItem {
  property1: Property;
  property2: Property;
  property3: Property;

  constructor(property1: Property, property2: Property, property3: Property) {
    this.property1 = property1;
    this.property2 = property2;
    this.property3 = property3;
  }
}

export class Property {
  name: string;
  value: string | string[];

  constructor(name: string, value: string | string[]) {
    this.name = name;
    this.value = value;
  }

  asString(): string {
    if (this.value instanceof Array) {
      return this.value.reduce(val => val + "\n");
    }
    return this.value;
  }

  asArray(): string[] {
    if (this.value instanceof Array) {
      return this.value;
    }
    return [this.value];
  }
}

