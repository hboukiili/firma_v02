import React, { useEffect, useState } from "react";
import { ReactSVG } from "react-svg";
import logo from "../../assets/logo.svg";
import menuIcon from "../../assets/sidebar.svg";
import { Accordion, AccordionItem, Button } from "@nextui-org/react";
import home_icn from "../../assets/SideBarIcons/Home.svg";
import field_icn from "../../assets/SideBarIcons/Field.svg";
import climate_icn from "../../assets/SideBarIcons/Climate.svg";
import irrigation_icn from "../../assets/SideBarIcons/irrigation.svg";
import yield_icn from "../../assets/SideBarIcons/Yield.svg";
import data_icn from "../../assets/SideBarIcons/data.svg";
import { Link, useLocation } from "react-router-dom";
import { Sidebar, Menu, MenuItem, SubMenu } from "react-pro-sidebar";
// import "./style.css"

import { styled, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import CssBaseline from "@mui/material/CssBaseline";
import MuiAppBar, { AppBarProps as MuiAppBarProps } from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import { Collapse } from "@mui/material";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import yieldIc from "../../assets/yieldIc.svg";
import fieldIc from "../../assets/fieldIc.svg";
import dashIc from "../../assets/dashIc.svg";
import irrIc from "../../assets/irrIc.svg";
import climateIc from "../../assets/climateIc.svg";

const drawerWidth = 240;

const SideBar = () => {
  const [open, setOpen] = useState(false);
  const [[open_0, open_1, open_2, open_3], setOpen_] = useState<boolean[]>([]);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    // if (open_0 || open_1 || open_2 || open_3) setOpen(true);
    setOpen(false);
  };

  const handleClick = (e) => {
    let idx = e.currentTarget.getAttribute("data-column");
    let tmp = [open_0, open_1, open_2, open_3];
    tmp[idx] = !tmp[idx];
    setOpen_(tmp);
    setOpen(true);
  };

  return (
    <div className="absolute w-[90%]">
      <Button
        color="primary"
        aria-label="open drawer"
        className="w-full ml-2 mt-2 h-[68px] bg-[#1E6F5C]"
        onFocus={handleDrawerOpen}
        // onFocusChange={handleDrawerClose}
      >
        <MenuIcon />
      </Button>

      <Drawer
        sx={{
          width: 0,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
            backgroundColor: "#1E6F5C",
          },
        }}
        variant="persistent"
        anchor="left"
        open={open}
      >
        <Button
          color="primary"
          className="w-full p-4 mt-4 mb-4  bg-[#1E6F5C]"
          onClick={handleDrawerClose}
        >
          <MenuIcon />
        </Button>
        <Divider />
        <List className="text-white">
          <ListItem key={"Dashboard"} disablePadding>
            <Link to="/farmer">
              <ListItemButton>
                <ListItemIcon>
                  <ReactSVG src={dashIc} />
                </ListItemIcon>
                <ListItemText primary={"Dashboard"} />
              </ListItemButton>
            </Link>
          </ListItem>

          <Divider />
          <ListItemButton onClick={handleClick} data-column={"0"}>
            <ListItemIcon>
              <ReactSVG src={fieldIc} />
            </ListItemIcon>
            <ListItemText primary="Field & Crop" />
            {open_0 ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
          <Collapse in={open_0} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {[
                { ic: "Field Managment", href: "/fieldmanagment" },
                { ic: "Crop Growth", href: "/cropgrowth" },
                { ic: "Soil", href: "/soil" },
              ].map((text, index) => (
                <ListItem key={text.ic} disablePadding>
                  <Link to={text.href}>
                    <ListItemButton>
                      <ListItemIcon>
                        {/* {index % 2 === 0 ? <InboxIcon /> : <MailIcon />} */}
                      </ListItemIcon>
                      <ListItemText primary={text.ic} />
                    </ListItemButton>
                  </Link>
                </ListItem>
              ))}
            </List>
          </Collapse>
          <Divider />
          <ListItemButton onClick={handleClick} data-column={"1"}>
            <ListItemIcon>
              <ReactSVG src={climateIc} />
            </ListItemIcon>
            <ListItemText primary="Climate" />
            {open_1 ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
          <Collapse in={open_1} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {["Climate", "Forecasting"].map((text, index) => (
                <ListItem key={text} disablePadding>
                  <Link className="w-full" to={"/" + text.toLowerCase()}>
                    <ListItemButton>
                      <ListItemIcon>
                        {/* {index % 2 === 0 ? <InboxIcon /> : <MailIcon />} */}
                      </ListItemIcon>
                      <ListItemText primary={text} />
                    </ListItemButton>
                  </Link>
                </ListItem>
              ))}
            </List>
          </Collapse>
          <Divider />
          <ListItemButton onClick={handleClick} data-column={"2"}>
            <ListItemIcon>
              <ReactSVG src={irrIc} />
            </ListItemIcon>
            <ListItemText primary="Irrigation" />
            {open_2 ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
          <Collapse in={open_2} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {["Water Stress", "Evapotranspiration", "Management"].map(
                (text, index) => (
                  <ListItem key={text} disablePadding>
                    <ListItemButton>
                      <ListItemIcon>
                        {/* {index % 2 === 0 ? <InboxIcon /> : <MailIcon />} */}
                      </ListItemIcon>
                      <ListItemText primary={text} />
                    </ListItemButton>
                  </ListItem>
                )
              )}
            </List>
          </Collapse>
          <Divider />
          <ListItemButton onClick={handleClick} data-column={"3"}>
            <ListItemIcon>
              <ReactSVG src={yieldIc} />
            </ListItemIcon>
            <ListItemText primary="Yield" />
            {open_3 ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
          <Collapse in={open_3} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {["Real Yield", "Forecccasting"].map((text, index) => (
                <ListItem key={text} disablePadding>
                  <ListItemButton>
                    <ListItemIcon>
                      {/* {index % 2 === 0 ? <InboxIcon /> : <MailIcon />} */}
                    </ListItemIcon>
                    <ListItemText primary={text} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Collapse>
        </List>
      </Drawer>
    </div>
  );
};

// const SideBar = () => {

// const [Isopn, SetIsopn] = useState(true);
// const [SmallScreen, SetScreen] = useState(false);
// const [IsFieldOpen, SetIsFieldOpen] = useState(false);
// const Location = useLocation();

// const SideBarstyleOnSmSc = "transition-all hidden overflow-hidden md:flex sm:hidden sm:w-full sm:flex grow flex-col   sm:bg-DarkGreen"
// const SideBarstyleOnLgSc = "w-full flex grow overflow-hidden flex-col bg-DarkGreen "

// useEffect(() => {
//     const handleResize = () => {
//         if (window.innerWidth <= 600)
//             SetScreen(!SmallScreen);
//     }
//     window.addEventListener('resize', handleResize);

//     // Clean up the event listener on component unmount
//     return () => {
//         window.removeEventListener('resize', handleResize);
//     };
// }, [window.innerWidth])
// return (<>
//      <div className="p-2 fixed top-0 z-[7000] flex justify-center items-center h-screen ">

//         <Sidebar collapsed={Isopn} backgroundColor="#134C39" width="15rem"
//             className="h-full rounded-lg overflow-hidden text-Green font-Myfont font-md relative"
//             collapsedWidth="5rem" >
//             <Menu className="absolute top-0 w-full h-[73px] bg-Lgreen" onClick={() => SetIsopn(!Isopn)}>
//                 <button className="w-full h-[73px] bg-white flex justify-center items-center">
//                     <ReactSVG className="" src={menuIcon} />
//                 </button>
//             </Menu>
//             <div className={Location.pathname === "/policymaker" ? "pt-16 h-[50%] flex flex-col justify-center" : "h-[50%] flex flex-col justify-between"}>
//                 {Location.pathname === "/policymaker" ?

//                     <Menu>
//                         <MenuItem href="/policymaker" icon={<ReactSVG src={home_icn} className="w-[1.2rem]" />} className="">
//                             Dashboard
//                         </MenuItem>
//                     </Menu>
//                     :
//                     <>
//                         <Menu>
//                             <MenuItem href="/" icon={<ReactSVG src={home_icn} className="w-[1.2rem]" />} className="">
//                                 Dashboard
//                             </MenuItem>
//                         </Menu>
//                         <Menu >
//                             <SubMenu icon={<ReactSVG className="w-[1.2rem]" src={field_icn} />} label="Field">
//                                 <MenuItem href="/addfield" className="bg-DarkGreen">
//                                     Add field
//                                 </MenuItem>
//                                 <MenuItem href="/cropgrowth" className="bg-DarkGreen">
//                                     Crop Growth
//                                 </MenuItem>
//                             </SubMenu>
//                         </Menu>
//                         <Menu>
//                             <SubMenu icon={<ReactSVG className="w-[1.1rem]" src={irrigation_icn} />} label="Irrigation">
//                                 <MenuItem className="bg-DarkGreen">

//                                 </MenuItem>
//                             </SubMenu>
//                         </Menu>
//                         <Menu>
//                             <SubMenu icon={<ReactSVG className="w-[1.3rem]" src={climate_icn} />} label="Climate">
//                                 <MenuItem className="bg-DarkGreen">

//                                 </MenuItem>
//                             </SubMenu>
//                         </Menu>
//                         <Menu>
//                             <SubMenu icon={<ReactSVG className="w-[1.2rem]" src={yield_icn} />} label="Yield">
//                                 <MenuItem className="bg-DarkGreen">

//                                 </MenuItem>
//                             </SubMenu>
//                         </Menu>
//                         <Menu>

//                             <MenuItem icon={<ReactSVG className="w-[1.3rem]" src={data_icn} />} href="/cropgrowth" className="bg-">
//                                 Data analytics
//                             </MenuItem>
//                         </Menu>
//                     </>
//                 }

//             </div>

//         </Sidebar>
//     </div>
// </>)
// return (
//     <>
//         <div className="absolute top-[18px] left-[100px]">
//             <ReactSVG className="w-[4rem] bg-DarkGreen" src={logo}></ReactSVG>
//         </div>
//         <div style={{
//             width: Isopn ? "15rem" : "5rem"
//         }}
//             className="fixed transition-all h-screen flex flex-col justify-between items-start top-0 z-[7000]">
//             <div className="h-[73px] w-full flex justify-center items-center bg-gray-50">
//                 <button onClick={() => {
//                     SetIsopn(!Isopn)
//                 }
//                 }>
//                     <ReactSVG className="hover:fill-Green fill-DarkGreen" src={menuIcon} />
//                 </button>
//             </div>
//             <div className={!Isopn ? SideBarstyleOnSmSc : SideBarstyleOnLgSc}>
//                 <div className="w-[15rem] pl-[1.3rem] h-full relative flex justify-center items-end flex-col">
//                     <ul className=" w-full gap-[2rem] flex flex-col justify-center items-start grow max-h-[80%]">
//                         <li style={Location.pathname == "/" ? { background: "#2F7047" } : { background: "none" }}
//                             className=" w-full h-[2.5rem] flex pl-[5px] items-center rounded-tl-full rounded-bl-full">
//                             <a onClick={() => SetIsopn(true)} href="/" className="flex gap-[2rem] text-Green font-Myfont font-smbld font-nrml items-center">
//                                 <div className="w-[2.2rem]  flex justify-center items-center">
//                                     <ReactSVG className="w-[1.3rem]" src={home_icn} />
//                                 </div>
//                                 Dashboard
//                             </a>
//                         </li>
//                         <li className="transition-all w-full  flex pl-[5px] items-center rounded-tl-full rounded-bl-full">
//                             <div onClick={() => {
//                                 SetIsopn(true)
//                                 SetIsFieldOpen(!IsFieldOpen);
//                             }}
//                                 className="flex flex-col justify-between cursor-pointer"
//                                 style={IsFieldOpen ? { height: "7rem" } : { height: "auto" }}>
//                                 <div className="h-full flex gap-[2rem] text-Green font-Myfont font-smbld items-center ">
//                                     <div className="w-[2.2rem]  flex justify-center items-center">
//                                         <ReactSVG className=" w-[1.3rem]" src={field_icn} />
//                                     </div>
//                                     Field & Crop
//                                 </div>
//                                 <div style={!IsFieldOpen ? { display: 'none', height: "0rem" } : { display: 'flex', height: "5rem" }}
//                                     className=" transition-all flex-col w-full gap-1 items-end">
//                                     <a className="text-Green font-Myfont font-lt" href="/addfield">Add Field</a>
//                                     <a className="text-Green font-Myfont font-lt" href="/cropgrowth">Crop Growth</a>
//                                 </div>

//                             </div>
//                         </li>
//                         <li className=" w-full h-[2.5rem] flex pl-[5px] items-center rounded-tl-full rounded-bl-full">
//                             <a href="" className="font-smbld flex gap-[2rem] text-Green font-Myfont  items-center">
//                                 <div className="w-[2.2rem]  flex justify-center items-center">
//                                     <ReactSVG className="w-[1.5rem]" src={irrigation_icn} />
//                                 </div>
//                                 Irrigation
//                             </a>
//                         </li>
//                         <li className=" w-full h-[2.5rem] flex pl-[5px] items-center rounded-tl-full rounded-bl-full">
//                             <a href="" className="font-smbld flex gap-[2rem] text-Green font-Myfont  items-center">
//                                 <div className="w-[2.2rem]  flex justify-center items-center">
//                                     <ReactSVG className="w-[1.5rem]" src={climate_icn} />
//                                 </div>
//                                 Climate
//                             </a>
//                         </li>
//                         <li className=" w-full h-[2.5rem] flex pl-[5px] items-center rounded-tl-full rounded-bl-full">
//                             <a href="" className="font-smbld flex gap-[2rem] text-Green font-Myfont font-nrml items-center">
//                                 <div className="w-[2.2rem]  flex justify-center items-center">
//                                     <ReactSVG className="w-[1.5rem]" src={yield_icn} />
//                                 </div>
//                                 Yield
//                             </a>
//                         </li>
//                     </ul>
//                 </div>
//             </div>

//         </div>
//     </>
// )
// }

export default SideBar;
