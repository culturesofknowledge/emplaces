import React from "react";
import HcEmPlaceItemHeader from "./HcEmPlaceItemHeader";

export default class HcEmTable extends React.Component<{ title: string, data: [{ [key: string]: string }] }> {
  keys: string[];
  constructor(props: { title: string, data: [{ [key: string]: any }] }) {
    super(props);
    const keys = new Set<string>();
    if (props.data.length > 0) {
      for (const row of props.data) {
        Object.keys(row).forEach(key => keys.add(key));
      }
      this.keys = Array.from(keys);
    }
    else {
      this.keys = [];
    }
  }

  render() {
    return (
      <div className="hcEmplDataBlock hcMarginBottom3">
        <HcEmPlaceItemHeader title={this.props.title} isH1={false} hasProv={true} />
        <div className="hcEmplList">
          <div className="hcEmplListHeader">
            {this.keys.map(key => {
              return <div key={Math.random()}>{key.charAt(0).toLocaleUpperCase() + key.slice(1)}</div>;
            })}
          </div>
          {this.props.data.map(row => {
            return <HcEmPlaceListRow key={Math.random()} data={row} keys={this.keys} />;
          })}
        </div>
      </div>
    );
  }
}

export class HcEmPlaceListRow extends React.Component<{ data: { [key: string]: string }, keys: string[] }> {
  render() {
    return (
      <div className="hcEmplListRow">
        {this.props.keys.map( key => {
          return <div key={Math.random()}>{this.props.data.hasOwnProperty(key) ? this.props.data[key] : ""}</div>
        })}
      </div>
    );
  }
}