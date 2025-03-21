import React from "react";
import { ReactSVG } from "react-svg";
import not from "./../../assets/notif.svg";
import out from "./../../assets/logout.svg";
import set from "./../../assets/sett.svg";
import api from "../../api/axios.js";
import Logo from "./../../assets/logo.svg";
import { useLocation } from "react-router-dom";
import {
  Button,
  Link,
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  NavbarMenu,
  NavbarMenuItem,
  NavbarMenuToggle,
} from "@nextui-org/react";

function NavBar() {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  const menuItems = [
    "Profile",
    "Dashboard",
    "Activity",
    "Analytics",
    "System",
    "Deployments",
    "My Settings",
    "Team Settings",
    "Help & Feedback",
    "Log Out",
  ];

  return (
    <Navbar
      className="rounded-full bg-white drop-shadow-xl"
      classNames={{ wrapper: "max-w-full" }}
      onMenuOpenChange={setIsMenuOpen}
    >
      <NavbarContent>
        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Close menu" : "Open menu"}
          className="sm:hidden"
        />
        <NavbarBrand>
          <ReactSVG className="w-[50px]" src={Logo} />
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="hidden sm:flex gap-10" justify="center">
        <NavbarItem>
          <Link className="font-smbld " color="foreground" href="/">
            Home
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link className="font-smbld " color="foreground" href="#">
            About
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link className="font-smbld " color="foreground" href="#">
            Product
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link className="font-smbld " color="foreground" href="#">
            Team
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link
            className="font-smbld "
            color="foreground"
            href="/documentation"
          >
            Documentation
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link className="font-smbld " color="foreground" href="#">
            Contact
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        <NavbarItem className="hidden lg:flex">
          <Link className="text-[#4FC38F]" href="/login">
            Login
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Button
            as={Link}
            className="rounded-full bg-[#4FC38F] text-white"
            href="/usertypes"
            variant="flat"
          >
            Sign Up
          </Button>
        </NavbarItem>
      </NavbarContent>
      <NavbarMenu>
        {menuItems.map((item, index) => (
          <NavbarMenuItem key={`${item}-${index}`}>
            <Link
              color={
                index === 2
                  ? "primary"
                  : index === menuItems.length - 1
                  ? "danger"
                  : "foreground"
              }
              className="w-full"
              href="#"
              size="lg"
            >
              {item}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </Navbar>
  );
}

const Header_ = () => {
  const location = useLocation();

  return (
    <div
      className={`${
        location.pathname == "/farmer" ? "max-w-[99%] " : "w-[99%]"
      } grow rounded-lg m-2 h-[68px] p-6 z-10  bg-gray-50 flex items-center justify-between self-end`}
    >
      <ReactSVG className="w-[50px]" src={Logo} />
      <div className="w-[10%] flex justify-between items-center mr-[3%]">
        <button>
          <ReactSVG className="w-[15px]" src={not} />
        </button>
        <button>
          <ReactSVG className="w-[15px]" src={set} />
        </button>
        <button
          onClick={() => {
            api.get("/api_auth/").then((res) => {
              console.log(res);
            });
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.clear();
            window.location.href = "/login"; // Redirect to the login page
          }}
        >
          <ReactSVG className="w-[15px]" src={out} />
        </button>
      </div>
    </div>
  );
};

const Header = () => {
  const location = useLocation()
  console.log(location.pathname)
  return (
    <>
    {location.pathname.startsWith("/farmer1") ? <Header_/> : <NavBar/>}
    </>
  );
};

export default Header;
