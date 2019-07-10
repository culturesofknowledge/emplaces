import React from 'react';
import HcEmPlaceItemHeader from './HcEmPlaceItemHeader';
import HcEmTable from './HcEmTable';
import HcEmPlaceCalendar from "./HcEmPlaceCalendar";
import HcEmPlaceHierarchy from './HcEmPlaceHierarchy';
import { match } from 'react-router';
import { SinglePlace } from '../../EMPlace';
import HcEmplaceCurrentHierchy from './HcEmPlaceCurrentHierarchy';

export default class HcLayoutEmplacesDetail extends React.Component<{ data: SinglePlace }> {

  render() {
    return <React.Fragment>
      <div className="hcContentContainer">
        <div className="hcEmpl2Col hcMarginBottom5">
          <div className="hcEmpl2Col1 basicSideMargin">
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmPlaceItemHeader title={this.props.data.title} isH1={true} hasProv={true} />
              <span>{this.props.data.alternateNameList.join(", ")}</span>
            </div>
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmplaceCurrentHierchy data={this.props.data.currentHierarchy} />
            </div>
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmPlaceItemHeader title="Location" isH1={false} hasProv={false} />
              <DataNotInSet />
            </div>
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmPlaceItemHeader title="Citation" isH1={false} hasProv={false} />
              <DataNotInSet />
            </div>
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmPlaceItemHeader title="Persistent URI" isH1={false} hasProv={false} />
              <DataNotInSet />
            </div>
            <ExternalLinks title="Authorities" links={this.props.data.alternateAuths} />
            <HcEmTable title="Name Attestations" data={[{ name: "Oppol", language: "(ger, lat)", date: "1226-1487", source: "Liber fundationis episcopatus Vratislaviensis" }]} />
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmPlaceItemHeader title="Calanders" isH1={false} hasProv={true} />
              <HcEmPlaceCalendar percent="23%" date="1584.01.28" />
            </div>
            <HcEmTable title="Connections" data={[{ name: "St. Adalbert", type: "Church", relation: "Located within" }]} />
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmPlaceItemHeader title="Related Resources" isH1={false} hasProv={false} />
              <ul>
                <li>Herder Institute: Historical-Topographical Atlas of Silesian Towns</li>
                <li>ARTFL: Diderot and d’Alembert, Encyclopédie (Opole)</li>
              </ul>
            </div>
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmPlaceItemHeader title="Bibliography" isH1={false} hasProv={false} />
              There are 16 publications associated with Opole.
                </div>
          </div>

          <div className="hcEmpl2Col2">
            <div className="hcEmplDataBlock hcMarginBottom3">
              <HcEmPlaceItemHeader title="Description" isH1={false} hasProv={false} />
              Opole is a city located in southern Poland on the Oder River (Odra). With a population of approximately 127,792 (January 2017), it is the capital of the Opole Voivodeship and also the seat of Opole County. With it long history dating back to the ninth century, Opole is considered to be one of the oldest towns in Poland.
            </div>
            <div className="hcEmplDataBlock hcMarginBottom3">
              <div className="hcEmplDataBlock hcMarginBottom3">
                <HcEmPlaceItemHeader title="Maps" isH1={false} hasProv={true} />
                <div className="hcEmplTabBar">
                  <div className="hcSelected">Current</div>
                  <div>1561</div>
                  <div>1608</div>
                  <div>1740</div>
                  <div>1794</div>
                </div>
                <div className="hcEmplEmbedBox"> </div>
              </div>
            </div>
            <HcEmPlaceHierarchy />
          </div>
        </div>

      </div>

      <div className="colorBgGreyLight">
        <div className="hcContentContainer">
          <div className="hcEmpl2Col hcMarginBottom5  hcMarginTop3">
            <div className="hcEmpl2Col1 basicSideMargin">
              <h2>About this record</h2>
              <div className="hcEmplDataBlock hcMarginBottom3">
                <HcEmPlaceItemHeader title="Feedback" isH1={false} hasProv={false} />
                Please email us your comments. We welcome contributions both from individual researchers and projects.
                </div>
            </div>
            <div className="hcEmpl2Col2 basicSideMargin">
              <div className="hcEmplDataBlock hcMarginBottom3">
                <br /><br /><br />
                <strong>Creator:</strong> Cultures of Knowledge <br />
                <strong> Contributors:</strong> Dariusz Gierczak, Arno Bosse <br />
                <strong>License:</strong> CC-BY (v3)
                </div>
              <div className="hcEmplDataBlock hcMarginBottom3">
                <HcEmPlaceItemHeader title="Export" isH1={false} hasProv={true} />
                Export record as <a href="#">CSV</a>, <a href="#">Excel</a>, <a href="#">Turtle-RDF</a>, <a href="#">GeoJSON</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>;
  }
}

class DataNotInSet extends React.Component {
  render() {
    return <span>{"{Data not in dataset}"}</span>
  }
}

class ExternalLinks extends React.Component<{ title: string, links: { label: string, uri: string }[] }> {
  render() {
    return (
    <div className="hcEmplDataBlock hcMarginBottom3">
      <HcEmPlaceItemHeader title={this.props.title} isH1={false} hasProv={false} />
      {
        this.props.links.map(link => {
        return <a key={Math.random()} href={link.uri}>{link.label} </a>;
      })}
    </div>
    );
  }
}