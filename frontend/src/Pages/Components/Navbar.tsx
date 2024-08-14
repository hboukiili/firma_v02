import { NavbarMenu, NavbarMenuItem, NavbarMenuToggle } from "@nextui-org/react";
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button } from "@nextui-org/react";
import { ReactSVG } from "react-svg";
import logo from "../../assets/logo.svg"
import React from "react";

const NavBar = () => {
    const [isMenuOpen, setIsMenuOpen] = React.useState(false);
    const menuItems = [
        "Home",
        "About Us",
        "Contact",
        "Sing Up",
    ];
    return (
        <Navbar className="font-Myfont bg-Lgreen" onMenuOpenChange={setIsMenuOpen}>
            <NavbarContent>
                <NavbarMenuToggle
                    aria-label={isMenuOpen ? "Close menu" : "Open menu"}
                    className="sm:hidden"
                />
                <NavbarBrand>
                    <ReactSVG className="w-16" src={logo}/>
                </NavbarBrand>
            </NavbarContent>

            <NavbarContent className="hidden sm:flex gap-8" justify="center">
                <NavbarItem>
                    <Link className="text-DarkGreen" href="#">
                        Home
                    </Link>
                </NavbarItem>
                <NavbarItem >
                    <Link href="#" className="text-DarkGreen" aria-current="page">
                        About Us
                    </Link>
                </NavbarItem>
                <NavbarItem>
                    <Link className="text-DarkGreen" href="#">
                        Contact
                    </Link>
                </NavbarItem>
            </NavbarContent>
            <NavbarContent justify="end">
                <NavbarItem >
                    <Link className="text-Green" href="/login">Login</Link>
                </NavbarItem>
                <NavbarItem className="hidden lg:flex">
                    <Button as={Link} onClick={() => window.location.href = '/usertypes'} className="bg-Green text-white" radius="full" href="#" variant="flat">
                        Sign Up
                    </Button>
                </NavbarItem>
            </NavbarContent>
            <NavbarMenu>
                {menuItems.map((item, index) => (
                    <NavbarMenuItem key={`${item}-${index}`}>
                        <Link
                            className={index != menuItems.length - 1 ? "w-full text-DarkGreen" : "w-full text-Green"}
                            href="#"
                            size="lg"
                        >
                            {item}
                        </Link>
                    </NavbarMenuItem>
                ))}
            </NavbarMenu>
        </Navbar>
    )
}

export default NavBar