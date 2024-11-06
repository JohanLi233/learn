import { Navbar as BootstrapNavbar, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
import "./css/navbar.css"

interface NavLink {
  name: string;
  path: string;
}

const navLinks: NavLink[] = [
  { name: "Home", path: "/" },
  { name: "Learn-News", path: "/learn-news" },
];

export default function Navbar() {
  return (
    <BootstrapNavbar bg="dark" variant="dark" expand="lg">
      <Nav className="me-auto center-nav">
        {" "}
        {navLinks.map((link) => (
          <Nav.Link as={Link} to={link.path} key={link.name}>
            {link.name}
          </Nav.Link>
        ))}
      </Nav>
    </BootstrapNavbar>
  );
}
