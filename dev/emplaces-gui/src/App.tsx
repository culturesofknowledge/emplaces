import React from 'react';
import HcHeaderTimbuctoo from './components/HcHeaderTimbuctoo';
import HcFooterTimbuctoo from './components/HcFooterTimbuctoo'
import './css/huc-connect-sets.css'
import './css/huc-data-entry.css'
import './css/huc-search.css'
import './css/remote.scss'
import { HcLayoutFacetResults } from './components/facetedsearch/HcLayoutFacetResults';

const App: React.FC = () => {
  return (
      <div className="App">
        <HcHeaderTimbuctoo></HcHeaderTimbuctoo>
        <HcLayoutFacetResults pageName="Place search"></HcLayoutFacetResults>
        <HcFooterTimbuctoo></HcFooterTimbuctoo>
      </div>
  );
}

export default App;
  
document.title = "EMPlaces";