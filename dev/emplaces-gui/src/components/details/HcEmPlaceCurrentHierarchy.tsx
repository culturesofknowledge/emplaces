import React from 'react';
import HcEmPlaceItemHeader from './HcEmPlaceItemHeader';

export default class HcEmplaceCurrentHierchy extends React.Component<{ data: string[] }> {
  state: {
    hierarchy: HTMLElement
  }

  constructor(props: { data: string[] }) {
    super(props);
    this.state = {
      hierarchy: React.createElement("br", null, null)
    }
  }

  componentDidUpdate(prevProps: { data: string[] }) {
    if (this.props !== prevProps) {
      let element;
      let prevElement;
      for (const item of this.props.data) {
        if (prevElement) {
          element = React.createElement("li", null, item, React.createElement("ul", null, prevElement));
        } else {
          element = React.createElement("li", null, item);
        }
        prevElement = element;
      }
      this.setState({ hierarchy: element });
    }
  }

  render() {
    return (
      <React.Fragment>
        <HcEmPlaceItemHeader title="Administrative hierarchy" isH1={false} hasProv={false} />
        <div className="hcEmplHierarchy">
          <ul>
            {this.state.hierarchy}
          </ul>
        </div>
      </React.Fragment>
    );
  }
}