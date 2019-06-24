import React from 'react';
import HcFacetBasic from "./HcFacetBasic";
import HcFacetTextSearch from './HcFacetTextSearch';
import { HcResultListHeader, HcResultList, HcResultSelectedFacets, HcResultListLegend, HcResultListPaging } from './HcResults';
import { SearchResult } from "./SearchResult";

export class HcLayoutFacetResults extends React.Component<{ pageName: String, data: SearchResult }> {

  render() {
    return (
      <div className="hcContentContainer">

        <div className="hcBasicSideMargin hcMarginTop4 hcMarginBottom1">
          <h1>{this.props.pageName}</h1>
        </div>

        <div className="hcLayoutFacet-Result hcBasicSideMargin hcMarginBottom15">

          <div className="hcLayoutFacets">
            <button type="button" name="button" id="showFacets" className="hcfixedSideButton">
              <img src="images/icons/icon-set-facets.svg" className="icon" alt="Click to open en close facets" />
            </button>

            <div className="hcLayoutFacetsToggel" id="hcLayoutFacetsToggel">
              <HcFacetTextSearch
                facetName="Text search"
              />

              {this.props.data.facets.map(facet => { return <HcFacetBasic key={Math.random()} facet={facet}/> })}

            </div>
          </div>

          <div className="hcLayoutResults">
            <HcResultListHeader totalResults={this.props.data.total} />
            <HcResultSelectedFacets />
            <HcResultListLegend />
            <HcResultList data={this.props.data.results} />
            <HcResultListPaging />


          </div>


        </div>
      </div>
    );
  }
}

