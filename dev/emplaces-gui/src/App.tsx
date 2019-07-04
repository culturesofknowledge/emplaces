import React from 'react';
import './css/huc-connect-sets.css'
import './css/huc-data-entry.css'
import './css/huc-search.css'
import './css/remote.scss'
import EMPlacesFacetedSearch from './EMPlacesFacetedSearch';


const App: React.FC = () => {
  return <EMPlacesFacetedSearch />
}

export default App;
  
document.title = "EMPlaces";
