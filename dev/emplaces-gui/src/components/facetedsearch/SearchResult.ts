import { Facet } from "./Facet";
import FullTextSearch from "./FullTextSearch"

export class SearchResult {
  facets: Facet[];
  fullTextSearch: FullTextSearch;
  results: ResultItem[];
  total: number;
  cursors: Cursors;
  constructor(total: number, data: ResultItem[], facets: Facet[], fullTextSearch: FullTextSearch, cursors: Cursors) {
    this.total = total;
    this.results = data;
    this.facets = facets;
    this.fullTextSearch = fullTextSearch;
    this.cursors = cursors;
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

export class Cursors {
  prevCursor: string | null;
  nextCursor: string | null;
  updateListener: (cursor: string | null) => void;
  
  constructor(prevCursor: string | null, nextCursor:string| null, updateListener: (cursor: string | null) => void) {
    this.prevCursor = prevCursor;
    this.nextCursor = nextCursor;
    this.updateListener = updateListener;

    this.prev= this.prev.bind(this);
    this.prev= this.next.bind(this);
  }

  prev(): void {
    this.updateListener(this.prevCursor);
  }

  next(): void {
    this.updateListener(this.nextCursor);
  }
}

