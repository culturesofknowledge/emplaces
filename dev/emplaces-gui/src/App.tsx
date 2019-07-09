import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import './css/huc-connect-sets.css'
import './css/huc-data-entry.css'
import './css/huc-search.css'
import './css/remote.scss'
import EMPlacesFacetedSearch from './EMPlacesFacetedSearch';
import HcHeaderTimbuctoo from './components/HcHeaderTimbuctoo';
import HcFooterTimbuctoo from './components/HcFooterTimbuctoo';
import EmPlacesDetail from './EMPlacesDetail';


const App: React.FC = () => {
  
   return <Router>
      <HcHeaderTimbuctoo />
      <Route exact path="/" component={EMPlacesFacetedSearch} />
      <Route path="/:uri" component={EmPlacesDetail} />
      <HcFooterTimbuctoo />
    </Router>;
}

export default App;
  
document.title = "EMPlaces";
