import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Overview" },
  { to: "/analyze", label: "Analyze" },
  { to: "/history", label: "History" }
];

export function NavBar() {
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">Editorial Intelligence Toolkit</p>
        <NavLink to="/" className="brandmark">
          IntegriNews
        </NavLink>
      </div>
      <nav className="navlinks" aria-label="Primary navigation">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) => (isActive ? "navlink active" : "navlink")}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}
