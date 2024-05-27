import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.js';
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'jquery/dist/jquery.js';
import './App.css';
import {createBrowserRouter,RouterProvider}from 'react-router-dom';
import { Home } from './components/Home';

function App() {
  
  const routes =createBrowserRouter([
    {path:'*',element:<Home/>}
  ]);
  return (

<RouterProvider router={routes}/>

);
}

export default App;
