import React from 'react'

export default class HcFacetTextSearch extends React.Component<{ facetName: String }> {
  render() {
    return (
      <div className="hcFacet">
        <div className="hcFacetTitle">{this.props.facetName}</div>
        <div className="hcFacetSearch">
          <input type="text" /> <button type="button" name="button">Search</button>
        </div>
      </div>
    );
  }
}