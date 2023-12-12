import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Login } from "./components/login";
import { Home } from "./components/home";
import { Navigation } from './components/navigation';
import { Logout } from './components/logout';
import Registration from './components/registration';
import {ProfilePage} from './components/profilepage';

function App() {
  return (
    <BrowserRouter>
      <Navigation></Navigation>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/registration" element={<Registration />} />
        <Route path="/profilepage" element={< ProfilePage/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
