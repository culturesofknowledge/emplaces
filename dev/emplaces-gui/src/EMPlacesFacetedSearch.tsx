import React from 'react';
import HcHeaderTimbuctoo from './components/HcHeaderTimbuctoo';
import HcFooterTimbuctoo from './components/HcFooterTimbuctoo'
import { HcLayoutFacetResults } from './components/facetedsearch/HcLayoutFacetResults';
import fetch from 'node-fetch'
import { SearchResult, ResultItem, Property, Cursors } from './components/facetedsearch/SearchResult';
import { instanceOfFacetData, Facet, FacetData } from './components/facetedsearch/Facet';
import { instanceOfEMPlace } from './EMPlace';
import FullTextSearch from './components/facetedsearch/FullTextSearch';

export default class FacetedSearch extends React.Component {
  dataSetId = "ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705";
  state: {
    data: SearchResult
  }
  query: string;

  private readonly collectionName = "em_PlaceList";

  constructor(props: { data?: GraphQlData }) {
    super(props);
    this.state = {
      data: {
        total: 0,
        results: [],
        facets: [],
        fullTextSearch: new FullTextSearch(() => this.executeQuery),
        cursors: new Cursors(null, null, () => {})
      }
    };
    this.query = "query emplaces ($esQuery: String, $cursor: ID ) {\n  dataSets {\n    ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705 {\n      em_PlaceList(elasticsearch:$esQuery, cursor:$cursor, count: 20) {\n        prevCursor\n        nextCursor\n        total\n        facets {\n          caption\n          options {\n            name\n            count\n          }\n        }\n        items {\n          em_preferredName {\n            value\n          }\n          title {\n            value\n          }\n          em_alternateAuthorityList {\n            items {\n              ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Source_desc {\n                title {\n                  value\n                }\n              }\n              ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Authority {\n                title {\n                  value\n                }\n              }\n            }\n          }\n          em_placeType {\n            ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_skos_Concept {\n              title {\n                value\n              }\n            }\n          }\n          em_alternateNameList {\n            items {\n              ... on Value {\n                value\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}"
  }

  componentDidMount() {
    this.executeQuery();
  }

  executeQuery(cursor?: string | null) {
    const postFilter = new EsFilter();
    const esQuery: any = {
      "aggs": {
        "Place type": new ESAggregation("em_placeType.title.value.raw"),
        "Calendars": new ESAggregation("em_hasAnnotationList.items.oa_hasBody.title.value.raw"),
        "Authority": new ESAggregation("em_alternateAuthorityList.items.title.value.raw")
      },
      "post_filter": postFilter
    }

    if (this.state.data.fullTextSearch.term !== "") {
      const filter = new ESTextFilter(this.state.data.fullTextSearch.term)
      esQuery["query"] = filter;
    }

    this.state.data.facets.forEach(facet => {
      if (facet.selectedOptions.length > 0 && esQuery.aggs[facet.caption]) {
        const fieldOfFacet = esQuery.aggs[facet.caption].aggs.name.terms.field;
        const filter = new EsShouldMatchFilter(fieldOfFacet, facet.selectedOptions)
        postFilter.addFilter(filter);

        Object.keys(esQuery.aggs).forEach((key, index) => {
          if (esQuery.aggs.hasOwnProperty(key)) {
            const agg: ESAggregation = esQuery.aggs[key];
            if (key !== facet.caption) {
              agg.addFilter(new EsShouldMatchFilter(fieldOfFacet, facet.selectedOptions));
            }
          }
        });
      }
    });

    fetch("https://repository.huygens.knaw.nl/v5/graphql", {
      "method": "POST",
      "body": JSON.stringify({
        "query": this.query,
        "operationName": "emplaces",
        "variables": {
          "esQuery": JSON.stringify(esQuery),
          "cursor": cursor
        }
      }),
      headers: { 'Content-Type': 'application/json' }
    }).then(resp => resp.json())
      .then(json => {
        if (this.instanceOfGraphQlData(json)) {
          const collection = this.getCollection(json);
          if (collection) {
            this.setState({ data: new SearchResult(this.getTotal(collection), this.getData(collection), this.getFacets(collection), this.getFullTextSearch(), this.getCursors(collection)) });
          }
        }
      });
  }

  render() {
    return (
      <div className="App">
        <HcHeaderTimbuctoo></HcHeaderTimbuctoo>
        <HcLayoutFacetResults pageName="Place search" data={this.state.data}></HcLayoutFacetResults>
        <HcFooterTimbuctoo></HcFooterTimbuctoo>
      </div>
    );
  }

  instanceOfGraphQlData(object: any): object is GraphQlData {
    return object["data"] && object["data"]["dataSets"];
  }

  getCursors(collection: GraphQLCollection): Cursors {
    return new Cursors(collection.prevCursor, collection.nextCursor, (cursor: string | null) => this.executeQuery(cursor));
  }

  getFullTextSearch(): FullTextSearch {
    return this.state.data.fullTextSearch.term !== "" ? this.state.data.fullTextSearch : new FullTextSearch(() => this.executeQuery());
  }

  getFacets(collection: GraphQLCollection): Facet[] {
    if (collection["facets"]) {
      const oldfacets: any = {};
      this.state.data.facets.forEach(facet => {
        oldfacets[facet.caption] = facet;
      });
      if (collection["facets"] instanceof Array && collection["facets"].every((item: any) => instanceOfFacetData(item))) {
        const facets: Facet[] = collection["facets"].map((facetData: FacetData) => new Facet(facetData, () => this.executeQuery()));
        facets.forEach(facet => {
          if (oldfacets[facet.caption]) {
            facet.selectedOptions = oldfacets[facet.caption].selectedOptions;
          }
        });
        return facets;
      }
    }
    return [];
  }

  getData(collection: GraphQLCollection): ResultItem[] {
    const resultData: ResultItem[] = [];

    if (collection && collection["items"]) {
      for (let item of collection["items"]) {
        if (instanceOfEMPlace(item)) {
          const property1 = new Property("PLACE", item.title.value);
          const property2 = new Property("PLACE TYPE", item.em_placeType && item.em_placeType.title && item.em_placeType.title.value ? item.em_placeType.title.value : "");
          const property3 = new Property("ALTERNATIVE NAMES", item.em_alternateNameList.items.map(value => value.value ? value.value : ""));
          resultData.push(new ResultItem(property1, property2, property3));
        }
      }
    }
    return resultData;
  }

  getCollection(data: GraphQlData): GraphQLCollection | null {
    if (data.data.dataSets) {
      const dataSets = data.data.dataSets;
      if (dataSets[this.dataSetId]) {
        const dataSet = dataSets[this.dataSetId];
        if (dataSet[this.collectionName] && this.instanceOfGraphQlCollection(dataSet[this.collectionName])) {
          return dataSet[this.collectionName];
        }
      }
    }
    return null;
  }

  instanceOfGraphQlCollection(object: any): object is GraphQLCollection {
    return object.hasOwnProperty("prevCursor") && object.hasOwnProperty("nextCursor")&& object.hasOwnProperty("total") && object.hasOwnProperty("facets") && object.hasOwnProperty("items");
  }

  getTotal(collection: GraphQLCollection): number {
    return collection["total"] ? collection["total"] : 0;
  }
}

class GraphQlData {
  "data": {
    "dataSets": any;
  }
}

class GraphQLCollection {
  "prevCursor": string | null
  "nextCursor": string | null
  "total": number
  "facets": []
  "items": any[]
}

class ESAggregation {
  filter: EsFilter;
  aggs: {};
  constructor(fieldPath: string) {
    this.filter = new EsFilter();
    this.aggs = {
      name: {
        terms: {
          field: fieldPath
        }
      }
    };
  }
  addFilter(filter: PropertyFilter): void {
    this.filter.addFilter(filter);
  }
}

class EsFilter {
  bool: {
    must: PropertyFilter[]
  }

  constructor() {
    this.bool = {
      must: []
    };
  }

  addFilter(filter: PropertyFilter): void {
    this.bool.must.push(filter);
  }
}

interface PropertyFilter { }

class ESTextFilter implements PropertyFilter {
  query_string: {
    fields: string[]
    query: string
  }
  constructor(term: string) {
    this.query_string = {
      fields: ["em_preferredName.value.fulltext^4", "em_alternateNameList.items.value.fulltext^60"],
      query: term
    };
  }
}

class EsShouldMatchFilter implements PropertyFilter {
  bool: any;
  constructor(fieldPath: string, values: string[]) {
    this.bool = {
      should: []
    }

    values.forEach(value => {
      const match: any = {};
      match[fieldPath] = value;
      this.bool.should.push({ match: match });
    });
  }
}

