import React, { ChangeEvent } from 'react'
import FullTextSearch from './FullTextSearch';

export default class HcFacetTextSearch extends React.Component<{ facetName: String, search:FullTextSearch }> {
  state: {
    term: string
  }
  constructor(props: { facetName: String, search:FullTextSearch }) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.state = { term: ""};
  }

  handleChange(event: ChangeEvent<HTMLInputElement>) {
    console.log(event.target.value)
    this.setState({term: event.target.value});
  }

  render() {
    return (
      <div className="hcFacet">
        <div className="hcFacetTitle">{this.props.facetName}</div>
        <div className="hcFacetSearch">
          <input type="text" value={this.state.term} onChange={this.handleChange}/> <button type="button" name="button" onClick= {() => this.props.search.search(this.state.term)}>Search</button>
        </div>
      </div>
    );
  }
}