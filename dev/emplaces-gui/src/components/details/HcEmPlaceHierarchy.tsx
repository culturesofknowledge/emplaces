import React from "react";
import HcEmPlaceItemHeader from './HcEmPlaceItemHeader';

export default class HcEmPlaceHierarchy extends React.Component {
  render() {
    return <div className="hcEmplDataBlock hcMarginBottom3">
      <HcEmPlaceItemHeader title="Historical Hierarchies" isH1={false} hasProv={true} />
      <div className="hcEmplTabBar">
        <div className="hcSelected">Administrative</div>
        <div className="">Ecclesiastical</div>
        <div className="hcTxtColorGreyMid">Military</div>
        <div className="hcTxtColorGreyMid">Judicial</div>
      </div>
      <div className="hcEmplEmbedBox hcEmplEmbedBoxaSide">
        <div className="hcEmplEmbedBoxNav">
          <div>1490-1521￼￼</div>
          <div>1521-1526</div>
          <div>1526-1742</div>
          <div>1742-1806</div>
        </div>
        <div className="hcEmplEmbedBoxContent">
          <HcEmPlHierarchyItem name="Holy Roman Empire" timeRange="0010 - 0129" />
          <HcEmPlHierarchyItem name="Bohemian Crown" timeRange="1100 - 1347" />
          <HcEmPlHierarchyItem name="Holy Roman Empire" timeRange="0010 - 0129" />
          <HcEmPlHierarchyItem name="Bohemian Crown" timeRange="1100 - 1347" />
        </div>
      </div>
    </div>
  }
}


class HcEmPlHierarchyItem extends React.Component<{ name: string, timeRange: string }> {
  render() {
    return (
      <div className="hcEmplacesHierarchyItem">
        <div>
          {this.props.name}
        </div>
        <svg height="10" width="100%">
          <line x1="50%" y1="0" x2="50%" y2="10" className="hcEmplacesHierarchyItemLine" />
          <circle cx="50%" cy="2" r="2" className="hcEmplacesHierarchyItemDot" />
        </svg>
        <div className="hcSmallTxt">
          {this.props.timeRange}
        </div>
        <svg height="10" width="100%">
          <line x1="50%" y1="0" x2="50%" y2="10" className="hcEmplacesHierarchyItemLine" />
        </svg>
      </div>
    );
  }
}