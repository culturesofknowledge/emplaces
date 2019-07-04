import React from 'react'
import HcResultItemEmPlaces from "./emplaces/HCResultItemEmPlaces"
import { ResultItem, Cursors } from './SearchResult';

export class HcResultListHeader extends React.Component<{ totalResults: number }>{

  render() {
    return (
      <div className="hcResultsHeader hcMarginBottom1">
        <div>{this.props.totalResults} Results</div>
        <div>
          <select className="" name="">
            <option value="">**Order options**</option>
          </select>
        </div>
      </div>
    );
  }
}


export class HcResultList extends React.Component<{ data: ResultItem[] }> {
  render() {
    return (
      <div className="hcList hcMarginBottom2">
        {this.props.data.map(result => {
          return <HcResultItemEmPlaces
            key={Math.random()}
            resultItemName={result.property1.asString()}
            resultItemAdministration=""
            resultItemType={result.property2.asString()}
            resultItemAltNames={result.property3.asArray()}
          />
        })}
      </div>
    );
  }
}

export class HcResultSelectedFacets extends React.Component {
  render() {
    return (
      <div className="hcMarginBottom2">
        <span className="hcSmallTxt hcTxtColorGreyMid">Selected facets:</span>
        <HcResultSelectedFacetsItem
          selectedFacetType="Fields of interest"
          selectedFacetValue="mathematics"
        />
      </div>
    );
  }
}

export class HcResultSelectedFacetsItem extends React.Component<{ selectedFacetType: String, selectedFacetValue: String }> {
  render() {
    return (
      <span className="hcSelectedFacet">
        <span className="hcSelectedFacetType">{this.props.selectedFacetType}</span>
        {this.props.selectedFacetValue}
      </span>
    );
  }
}

export class HcResultListLegend extends React.Component {
  render() {
    return (
      <div className="hcList">
        <div className="hcListHeader">
          <div className="hcLabel hcListItemLong">Place </div>
          <div className="hcLabel">Place type</div>
          <div className="hcLabel">Alternative names</div>
        </div>
      </div>
    );
  }
}

export class HcResultListPaging extends React.Component<{ data: Cursors }> {
  render() {
    return (
      <div className="hcPagination">
        {/* eslint-disable-next-line */}
        <div><a className={ this.props.data.prevCursor ? "" : "disabled" } href="#" onClick={() => this.props.data.prev()}>← Previous</a></div>
        {/* eslint-disable-next-line */}
        <div><a className={ this.props.data.nextCursor ? "" : "disabled" } href="#" onClick={() => this.props.data.next()}>Next →</a></div>
      </div>
    );
  }
}