import React from 'react';
import { match } from 'react-router';
import HcLayoutEmplacesDetail from './components/details/HcLayoutEmplacesDetail';
import {SinglePlace, Link, QualifiedRelation, MapLocation, Period} from './EMPlace';
import { instanceOfGraphQlData, GraphQlData } from './GraphQlData';

export default class EmPlacesDetail extends React.Component<{ match: match<{ uri: string }> }> {
  private readonly collection = "em_Place";
  private readonly dataSetId = "ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710";
  private readonly query = "query singlePlace($uri: String!) {\n  dataSets {\n    ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710 {\n      em_Place(uri: $uri) {\n        em_preferredName {\n          value\n        }\n        title {\n          value\n        }\n        em_alternateNameList {\n          items {\n            ... on Value {\n              value\n            }\n          }\n        }\n        em_hasRelationList {\n          items {\n            ...recursiveRelation\n          }\n        }\n        em_settingList {\n          items {\n            em_location {\n              title {\n                value\n              }\n              wgs84_pos_lat {\n                value\n              }\n              wgs84_pos_long {\n                value\n              }\n            }\n            em_when {\n              rdfs_label {\n                value\n              }\n              em_timespanList {\n                items {\n                  em_latestStart {\n                    value\n                  }\n                  em_earliestEnd {\n                    value\n                  }\n                }\n              }\n            }\n          }\n        }\n        em_source {\n          ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Authority {\n            title {\n              value\n            }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment recursiveRelation on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Qualified_relation {\n  ...relationFields\n  em_relationTo {\n    ...relatedPlace\n    ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n      em_hasRelation {\n        ...relationFields\n        em_relationTo {\n          ...relatedPlace\n          ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n            em_hasRelation {\n              ...relationFields\n              em_relationTo {\n                ...relatedPlace\n                ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n                  em_hasRelation {\n                    ...relationFields\n                    em_relationTo {\n                      ...relatedPlace\n                      ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n                        em_hasRelation {\n                          ...relationFields\n                          em_relationTo {\n                            ...relatedPlace\n                            ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n                              em_hasRelation {\n                                ...relationFields\n                                em_relationTo {\n                                  ...relatedPlace\n                                  ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n                                    em_hasRelation {\n                                      ...relationFields\n                                      em_relationTo {\n                                        ...relatedPlace\n                                        ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n                                          em_hasRelation {\n                                            ...relationFields\n                                            em_relationTo {\n                                              ...relatedPlace\n                                              ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n                                                em_hasRelation {\n                                                  ...relationFields\n                                                  em_relationTo {\n                                                    ...relatedPlace\n                                                    ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n                                                      em_hasRelation {\n                                                        ...relationFields\n                                                        em_relationTo {\n                                                          ...relatedPlace\n                                                          ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n                                                            em_hasRelation {\n                                                              ...relationFields\n                                                              em_relationTo {\n                                                                ...relatedPlace\n                                                              }\n                                                            }\n                                                          }\n                                                        }\n                                                      }\n                                                    }\n                                                  }\n                                                }\n                                              }\n                                            }\n                                          }\n                                        }\n                                      }\n                                    }\n                                  }\n                                }\n                              }\n                            }\n                          }\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment relationFields on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Qualified_relation {\n  em_relationType {\n    title {\n      value\n    }\n  }\n  em_when {\n    rdfs_label {\n      value\n    }\n    em_timespanList {\n      items {\n        em_latestStart_ {\n          value\n        }\n        em_earliestEnd_ {\n          value\n        }\n      }\n    }\n  }\n}\n\nfragment relatedPlace on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_em_Place {\n  title {\n    value\n  }\n  em_preferredName {\n    value\n  }\n  em_placeCategory {\n    ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710_skos_Concept {\n      rdfs_label {\n        value\n      }\n    }\n  }\n}";
  uri: string;
  state: {
    data: SinglePlace
  };


  constructor(props: { match: match<{ uri: string }> }) {
    super(props);
    this.uri = decodeURIComponent(props.match.params.uri);
    this.state = { data: this.dummySinglePlace() };
  }

  componentDidMount() {
    fetch("https://repository.huygens.knaw.nl/v5/graphql", {
      "method": "POST",
      "body": JSON.stringify({
        "query": this.query,
        "operationName": "singlePlace",
        "variables": {
          "uri": this.uri
        }
      }),
      headers: { 'Content-Type': 'application/json' }
    }).then(resp => resp.json())
      .then(json => {
        if (instanceOfGraphQlData(json)) {
          this.setState({ data: this.createSinglePlace(json) });
        }
      });
  }

  createSinglePlace(data: GraphQlData): SinglePlace {
    const dataSets = data.data.dataSets;

    if (dataSets[this.dataSetId]) {
      const dataSet = dataSets[this.dataSetId];

      if (dataSet[this.collection]) {
        const collection = dataSet[this.collection];

        return new SinglePlace(this.getTitle(collection), this.getAlternateNames(collection), this.getHierarchies(collection), this.getAuthorities(collection), this.getLocations(collection));
      }
    }

    return this.dummySinglePlace();
  }

  getLocations(collection: any): MapLocation[] {
    if(collection["em_settingList"]) {
      return collection["em_settingList"]["items"].map((setting:any) => {
        const location = setting["em_location"];
        const when = setting["em_when"]["em_timespanList"]["items"];
        return new MapLocation(location["wgs84_pos_lat"], location["wgs84_pos_long"], when.map((span:any) => new Period(span["em_latestStart"], span["em_earliestEnd"])))
      })
    }

    return  []
  }

  getAuthorities(collection: any): Link[] {
    
    if(collection.hasOwnProperty("em_source")) {
      return [new Link(collection["em_source"]["title"].value, "#")];
    }

    return [];
  }

  getAlternateNames(collection: any): string[] {
    return collection["em_alternateNameList"] ? collection["em_alternateNameList"]["items"].map( (item: { [x: string]: any; }) => item["value"]) : [];
  }

  getTitle(collection: any): string {
    if(collection["em_preferredName"]) {
      return collection["em_preferredName"]["value"];
    } 
    
    return collection["title"]["value"];
  }

  getHierarchies(collection: any) : QualifiedRelation[] {
    return collection["em_hasRelationList"]["items"];
  }

  dummySinglePlace(): SinglePlace {
    return {
      title: "{title}",
      alternateNameList: ["{alternateNames}"],
      currentHierarchy: [], 
      alternateAuths: [],
      currentLocation: undefined,
    };
  }

  render() {
    return <HcLayoutEmplacesDetail data={this.state.data} />;
  }
}