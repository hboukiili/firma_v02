import React, { Suspense, useEffect, useRef, useState } from "react";
import NavBar from "../Components/Navbar";
import Slider_ from "./Slider";
import { Button, Input, Textarea } from "@nextui-org/react";
import about_img from "../../assets/about.jpg";
import typesBg from "../../assets/typesBg.png";
import about_img2 from "../../assets/about2.png";
import Farmer_icn from "../../assets/Farmer.svg";
import Policymake_icn from "../../assets/Policymaker.svg";
import Academic_icn from "../../assets/Academic.svg";
import { ReactSVG } from "react-svg";
import Header from "../Components/Header";
import { Carousel, Form, Space } from "antd";
import Slide_bg from "../../../assets/slide.jpg";
import o1_bg from "../../assets/03.jpg";
import o2_bg from "../../assets/04.jpg";
import o5_bg from "../../assets/o5.jpg";
import fp_bg from "../../assets/fp.jpg";
import ap_bg from "../../assets/ap.jpg";
import pp_bg from "../../assets/pp.jpg";
import tt_bg from "../../assets/testt.png";
import vd from "../../assets/ourStory.mp4";
import gr_bg from "../../assets/gridBg_.png";
import profil_pic from "../../assets/blank.png";
import { motion, useAnimation, useInView, useScroll } from "framer-motion";
import { TypeAnimation } from "react-type-animation";
import Slider from "react-infinite-logo-slider";
import logo0 from "../../assets/Plogos/1.png";
import logo1 from "../../assets/Plogos/2.png";
import logo2 from "../../assets/Plogos/3.png";
import logo3 from "../../assets/Plogos/4.png";
import logo4 from "../../assets/Plogos/5.png";
import logo5 from "../../assets/Plogos/6.png";
import logo6 from "../../assets/Plogos/7.png";
import AnimatedCursor from "react-animated-cursor";

const InfiniteLogos = () => {
  return (
    <Slider
      width="250px"
      duration={40}
      pauseOnHover={true}
      blurBorders={false}
      blurBoderColor={"#fff"}
    >
      <Slider.Slide>
        <img src={logo0} alt="any" className="w-36" />
      </Slider.Slide>
      <Slider.Slide>
        <img src={logo1} alt="any2" className="w-36" />
      </Slider.Slide>
      <Slider.Slide>
        <img src={logo2} alt="any3" className="w-36" />
      </Slider.Slide>
      <Slider.Slide>
        <img src={logo3} alt="any" className="w-36" />
      </Slider.Slide>
      <Slider.Slide>
        <img src={logo4} alt="any2" className="w-36" />
      </Slider.Slide>
      <Slider.Slide>
        <img src={logo5} alt="any3" className="w-36" />
      </Slider.Slide>
      <Slider.Slide>
        <img src={logo6} alt="any3" className="w-36" />
      </Slider.Slide>
    </Slider>
  );
};

const Contact = () => {
  const [form] = Form.useForm<{}>();

  return (
    <div className="w-full flex gap-16 justify-center pt-32 pb-20 bg-white z-10 font-Myfont">
      <div className="flex flex-col gap-6">
        <p className="text-[48px] font-bld leading-[70px]">
          We're here to help. <br />
          Contact us now <br />
          for more information.
        </p>
        <p className="text-[20px]">crsa@um6p.ma</p>
        <p className="text-[20px]">+123 456 789</p>
        <p className="text-[20px]">123 Street 456 </p>
      </div>
      <div className="w-[45%]">
        <Form form={form} layout="vertical" autoComplete="off">
          <Form.Item name={"fullName"} label="Full name">
            <Input radius="full" variant="bordered" placeholder="Full name" />
          </Form.Item>

          <Form.Item name="email" label="Your Email">
            <Input
              radius="full"
              variant="bordered"
              placeholder="example@yourmail.com"
            />
          </Form.Item>

          <Form.Item name="subject" label="Subject">
            <Input
              size="lg"
              radius="full"
              variant="bordered"
              placeholder="How can we Help"
            />
          </Form.Item>

          <Form.Item name="message" label="Message">
            <Textarea radius="full" variant="bordered" placeholder="Message" />
          </Form.Item>
          <Button className="text-white bg-[#4FC38F] w-[200px] rounded-full">
            Read More
          </Button>
        </Form>
      </div>
    </div>
  );
};

const PartnersSc = () => {
  const ref_ = useRef(null);
  const isInview = useInView(ref_, { once: true });
  return (
    <div
      ref={ref_}
      className=" font-Myfont w-full flex flex-col bg-white z-20 items-center gap-14"
    >
      <div className="flex flex-col justify-center items-center">
        {isInview && (
          <TypeAnimation
            sequence={["we work with the best partners", 1000]}
            speed={1}
            className="text-[40px] text-[#494949] font-bld"
            // style={{ fontSize: "2em" }}
            repeat={0}
            cursor={false}
          />
        )}
        <p className="text-[22px] text-[#A6A6A6]">
          FIRMA collaborates with top industry leaders to bring you the most
          advanced solutions for sustainable agriculture.
        </p>
      </div>
      <InfiniteLogos />
    </div>
  );
};

interface card {
  name: string;
  icn: any;
}

const Card = (data: card) => {
  return (
    <div className="w-[260px] p-2 h-[440px] bg-white flex justify-center items-center flex-col gap-[25px] rounded-lg">
      <h1 className="font-Myfont font-bld text-DarkGreen">{data.name}</h1>
      <ReactSVG src={data.icn} />
      <p className="font-Myfont font-lt text-[10px] max-w-[180px] text-center">
        Lorem Ipsum is simply dummy text of the printing and typesetting
        industry. Lorem Ipsum has been the industry's{" "}
      </p>
      <div>
        {/* {data.name === 'Farmer' || data.name === 'Academic' && */}
        <p className="font-Myfont font-bld text-[24px] text-[#F97373]">
          {" "}
          49$/ <span className="font-Myfont text-[16px]">m</span>
        </p>
      </div>
      <ul className="space-y-[10px]">
        <li className="font-Myfont text-[10px] font-smbld">
          Lorem Ipsum is simply dummy
        </li>
        <li className="font-Myfont text-[10px] font-smbld">
          Lorem Ipsum is simply dummy
        </li>
        <li className="font-Myfont text-[10px] font-smbld">
          Lorem Ipsum is simply dummy
        </li>
        <li className="font-Myfont text-[10px] font-smbld">
          Lorem Ipsum is simply dummy
        </li>
      </ul>
      <Button
        radius="full"
        className=" max-w-[140px] bg-Green font-Myfont text-white"
      >
        Unlock
      </Button>
    </div>
  );
};
const hovereff = {
  normal: "transition-all duration-250 ease-in-out",
};
const FrmPro = () => {
  return (
    <div className="group flex flex-col grow h-full max-w-[33.3333333%] gap-2">
      <div
        className={`${hovereff.normal} bg-[#4FC38F] group h-[50%] rounded-[30px] rounded-br-[150px] group-hover:rounded-br-[30px] flex flex-col pt-10 items-center relative`}
      >
        <div className="max-w-[80%] flex flex-col gap-4">
          <p className="font-bld text-[36px] text-white">For Farmers</p>
          <p className="text-[24px] font-md text-justify text-[#DBFFEF]">
            FIRMA helps farmers improve irrigation and fertilization practices
            with data-driven insights, tailored to field-specific conditions.
          </p>
        </div>
        <Button
          size="lg"
          className={`
            absolute bottom-0 left-0 rounded-none rounded-tr-[30px] rounded-bl-[30px] bg-[#A0F0CC] text-[#033323] font-bld w-[165px]`}
        >
          Explore
        </Button>
      </div>
      <img
        src={fp_bg}
        alt=""
        className={`rounded-[30px] rounded-br-[150px] max-h-[50%] group-hover:rounded-br-[30px] ${hovereff.normal}`}
      />
    </div>
  );
};

const PlyPro = () => {
  return (
    <div
      className={`group flex flex-col grow h-full max-w-[33.3333333%] gap-2`}
    >
      <img
        src={pp_bg}
        alt=""
        className={`${hovereff.normal} rounded-[30px] rounded-tr-[150px] group-hover:rounded-tr-[30px] max-h-[50%]`}
      />
      <div
        className={`${hovereff.normal} bg-[#4C6CE2] h-[50%] rounded-[30px] rounded-tr-[150px] group-hover:rounded-tr-[30px] flex flex-col pt-10 items-center relative`}
      >
        <div className="max-w-[80%] flex flex-col gap-4">
          <p className="font-bld text-[36px] text-white">For Policymakers</p>
          <p className="text-[24px] font-md text-justify text-[#C8D2FB]">
            A decision-support tool that enables policymakers to manage water
            resources and agricultural policies based on real-time and
            historical data.
          </p>
        </div>
        <Button
          size="lg"
          className="absolute bottom-0 left-0 rounded-none rounded-tr-[30px] rounded-bl-[30px] bg-[#C8D2FB] text-[#283871] font-bld w-[165px]"
        >
          Explore
        </Button>
      </div>
    </div>
  );
};

const AcdPro = () => {
  return (
    <div className="group flex flex-col grow h-full max-w-[33.3333333%] gap-2">
      <div
        className={`${hovereff.normal} bg-[#E59766] h-[50%] rounded-[30px] rounded-br-[150px] group-hover:rounded-br-[30px] flex flex-col pt-10 items-center relative`}
      >
        <div className="max-w-[80%] flex flex-col gap-4">
          <p className="font-bld text-[36px] text-white">For Academics</p>
          <p className="text-[24px] font-md text-justify text-[#FFFEE1]">
            A comprehensive data platform for academics to conduct research on
            agriculture, water management, and sustainability.
          </p>
        </div>
        <Button
          size="lg"
          className="absolute bottom-0 left-0 rounded-none rounded-tr-[30px] rounded-bl-[30px] bg-[#FFFEE1] text-[#7B4320] font-bld w-[165px]"
        >
          Explore
        </Button>
      </div>
      <img
        src={ap_bg}
        alt=""
        className={`${hovereff.normal} rounded-[30px] rounded-bl-[150px] group-hover:rounded-bl-[30px] max-h-[50%]`}
      />
    </div>
  );
};

const ProductSc = () => {
  const ref_ = useRef(null);
  const isInview = useInView(ref_, { once: true });
  const root = useAnimation();
  // console.log(scrollX.animation())
  useEffect(() => {
    if (isInview) {
      root.start("end");
    }
  }, [isInview]);
  return (
    <div
      ref={ref_}
      className="h-screen font-Myfont p-4 flex flex-col  z-10 bg-[#F2F9F3]"
    >
      <div
        // variants={{
        //   start: { opacity: 0 },
        //   end: { opacity: 1 },
        // }}
        // initial="start"
        // animate={root}
        className="overflow-hidden  pl-14"
        // transition={{ delay: 0.3, duration: 0.5 }}
      >
        {/* <p className="text-[64px] text-[#494949] font-bld min-w-[900px] w-[900px]">
          How FIRMA Works for You
        </p> */}
        {isInview && (
          <TypeAnimation
            sequence={[" How FIRMA Works for You", 1000]}
            speed={1}
            className="text-[64px] text-[#494949] font-bld"
            // style={{ fontSize: "2em" }}
            repeat={0}
            cursor={false}
          />
        )}
        <p className="font-lt text-[#494949] min-w-[900px] w-[900px]">
          FIRMA offers specialized tools and services tailored to the unique
          needs of Policymakers, Farmers, and Academics, helping each group
          leverage advanced data for smarter decisions.
        </p>
      </div>
      <motion.div
        variants={{
          start: { opacity: 0, y: 575 },
          end: { opacity: 1, y: 0 },
        }}
        initial="start"
        animate={root}
        transition={{ delay: 0.96, duration: 0.7 }}
        className="grow max-w-[1800px] flex self-center gap-2 p-4 pt-8 "
      >
        <FrmPro />
        <PlyPro />
        <AcdPro />
      </motion.div>
    </div>
  );
};

const HeroSc = () => {
  return (
    <div className="w-[98.5%] h-full font-Myfont fixed z-0">
      <Carousel
        autoplaySpeed={3000}
        speed={1300}
        effect="fade"
        className="overflow-hidden rounded-[30px] h-[830px]"
        autoplay
      >
        <div className="relative w-full h-[830px] bg-black font-Myfont">
          <div className="absolute flex flex-col justify-between h-full pb-7 pl-20 pt-4 top-0 bg-whte z-50 w-[800px] bg-[#ffffff1a] backdrop-blur-lg">
            <div>
              <p className="text-[180px] font-bld text-white leading-[95%]">
                FIRMA
              </p>
              <p className="text-[32px] font-smbld text-[#E4E171] ">
                Innovative Solutions <br /> for Smarter Agriculture
              </p>
            </div>
            <div className="flex flex-col gap-4  rounded-2xl p-4 w-[80%]">
              <p className="text-[#ffffff] leading-6 text-justify text-[18px] line-clamp-4 font-nrml">
                Improve water efficiency and agricultural productivity with
                FIRMA's innovative platform. Combining modern technologies like
                remote sensing and machine learning, FIRMA offers real-time data
                insights, predictive modeling, and smart irrigation solutions.
                Optimize resource management, enhance crop yield, and contribute
                to sustainable agriculture practices, ensuring better
                decision-making for farmers, policymakers, and researchers
                alike.
              </p>
              <div className="flex gap-2">
                <Button className="rounded-full w-[150px] text-[#033323] bg-[#E6FEE8]">
                  Read more
                </Button>
                <Button className="rounded-full w-[150px] text-[#033323] bg-white">
                  Get started
                </Button>
              </div>
            </div>
          </div>
          <img
            src={o5_bg}
            className="object-cover w-full h-full opacity-75 transform scale-x-[-1] scale-y--1]"
          />
        </div>
        <div className="relative w-full h-[830px] bg-black font-Myfont">
          <div className="absolute flex flex-col justify-between h-full pb-7 pl-20 pt-4 top-0 bg-whte z-50 w-[800px] bg-[#ffffff1a] backdrop-blur-lg">
            <div>
              <p className="text-[180px] font-bld text-white leading-[95%]">
                FIRMA
              </p>
              <p className="text-[32px] font-smbld text-[#E4E171] ">
                Innovative Solutions <br /> for Smarter Agriculture
              </p>
            </div>
            <div className="flex flex-col gap-4  rounded-2xl p-4 w-[80%]">
              <p className="text-[#ffffff] leading-6 text-justify text-[18px] line-clamp-4 font-nrml">
                Improve water efficiency and agricultural productivity with
                FIRMA's innovative platform. Combining modern technologies like
                remote sensing and machine learning, FIRMA offers real-time data
                insights, predictive modeling, and smart irrigation solutions.
                Optimize resource management, enhance crop yield, and contribute
                to sustainable agriculture practices, ensuring better
                decision-making for farmers, policymakers, and researchers
                alike.
              </p>
              <div className="flex gap-2">
                <Button className="rounded-full w-[150px] text-[#033323] bg-[#E6FEE8]">
                  Read more
                </Button>
                <Button className="rounded-full w-[150px] text-[#033323] bg-white">
                  Get started
                </Button>
              </div>
            </div>
          </div>
          <img
            src={o1_bg}
            className="object-cover w-full h-full opacity-75 transform"
          />
        </div>
        <div className="relative w-full h-[830px] bg-black font-Myfont">
          <div className="absolute flex flex-col justify-between h-full pb-7 pl-20 pt-4 top-0 bg-whte z-50 w-[800px] bg-[#ffffff1a] backdrop-blur-lg">
            <div>
              <p className="text-[180px] font-bld text-white leading-[95%]">
                FIRMA
              </p>
              <p className="text-[32px] font-smbld text-[#E4E171] ">
                Innovative Solutions <br /> for Smarter Agriculture
              </p>
            </div>
            <div className="flex flex-col gap-4  rounded-2xl p-4 w-[80%]">
              <p className="text-[#ffffff] leading-6 text-justify text-[18px] line-clamp-4 font-nrml">
                Improve water efficiency and agricultural productivity with
                FIRMA's innovative platform. Combining modern technologies like
                remote sensing and machine learning, FIRMA offers real-time data
                insights, predictive modeling, and smart irrigation solutions.
                Optimize resource management, enhance crop yield, and contribute
                to sustainable agriculture practices, ensuring better
                decision-making for farmers, policymakers, and researchers
                alike.
              </p>
              <div className="flex gap-2">
                <Button className="rounded-full w-[150px] text-[#033323] bg-[#E6FEE8]">
                  Read more
                </Button>
                <Button className="rounded-full w-[150px] text-[#033323] bg-white">
                  Get started
                </Button>
              </div>
            </div>
          </div>
          <img
            src={o2_bg}
            className="object-cover w-full h-full opacity-75 transform"
          />
        </div>
        
      </Carousel>
    </div>
  );
};

const OurStory = () => {
  const videoR = useRef<HTMLVideoElement>(null);
  const ref_ = useRef(null);
  const isInview = useInView(ref_, { once: true });
  const root = useAnimation();
  // console.log(scrollX.animation())
  useEffect(() => {
    if (isInview) {
      root.start("end");
    }
  }, [isInview]);

  return (
    <div
      ref={ref_}
      className="font-Myfont h-screen w-full p-4 flex justify-center items-center bg-white z-20"
    >
      <div className="w-full h-full flex rounded-[30px] overflow-hidden items-center gap-8">
        <motion.div
          variants={{
            start: { opacity: 0, width: 0 },
            end: { opacity: 1, width: "45%" },
          }}
          initial="start"
          animate={root}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="max-w-[42%] flex flex-col gap-6 items-start pl-16  justify-center "
        >
          {isInview && (
            <TypeAnimation
              sequence={["Our Story", 1000]}
              speed={1}
              className="font-bld text-[100px] text-[#494949]"
              repeat={0}
              cursor={false}
            />
          )}
          <p className="text-[20px] w-[90%] text-[#494949] text-justify">
            Improve water efficiency and agricultural productivity with FIRMA's
            innovative platform. Combining modern technologies like remote
            sensing and machine learning, FIRMA offers real-time data insights,
            predictive modeling, and smart irrigation solutions. Optimize
            resource management, enhance crop yield, and contribute to
            sustainable agriculture practices, ensuring better decision-making
            for farmers, policymakers, and researchers alike.
          </p>
          <Button className="text-white bg-[#4FC38F] w-[200px] rounded-full">
            Read More
          </Button>
        </motion.div>
        <div className=" h-full grow bg-[#919191]">
          <video
            className="object-cover h-full opacity-80 "
            autoPlay
            loop
            muted
          >
            <source src={vd} type="video/mp4" />
          </video>
        </div>
      </div>
    </div>
  );
};

const TeamCard = () => {
  return (
    <div
      className={`${hovereff.normal} relative w-[370px] flex flex-col hover:h-[545px]
      h-[460px] cursor-pointer rounded-[25px] rounded-tr-[85px] hover:rounded-tr-[25px] overflow-hidden mt-4 bg-[#4C6CE2]`}
    >
      <img
        className="z-10 grayscale max-h-[460px] fil"
        src={profil_pic}
        alt=""
      />
      <div className="z-0 h-[88px] w-full absolute bottom-0 font-Myfont font-bld text-[20px] text-white p-4">
        FIRSTNAME NAME
        <p className="font-nrml text-[#A9B9F4] text-[16px]">
          Back-end Developer{" "}
        </p>
      </div>
    </div>
  );
};

const Team = () => {
  const ref_ = useRef(null);
  const isInview = useInView(ref_, { once: true });
  const root = useAnimation();
  // console.log(scrollX.animation())
  useEffect(() => {
    if (isInview) {
      root.start("end");
    }
  }, [isInview]);
  return (
    <div className="h-screen w-full font-Myfont p-4 z-10 bg-[#F2F9F3]">
      <div className="w-full flex pl-4  h-[260px] bg-[#4FC38F] rounded-[30px] justify-between">
        <div ref={ref_} className="font-bld text-[100px] text-white pl-10 ">
          {isInview && (
            <TypeAnimation
              sequence={["Meet Our Team", 1000]}
              speed={1}
              className="text-[64px] text-[#ffffff] font-bld "
              // style={{ fontSize: "2em" }}
              repeat={0}
              cursor={false}
            />
          )}

          <p className="font-nrml text-[20px] text-white">
            Get to know the passionate experts behind FIRMA, dedicated to
            transforming <br /> agriculture through innovation and technology.
          </p>
        </div>
        <img className="h-full" src={gr_bg} alt="" />
      </div>
      <div className="w-full flex gap-2">
        <TeamCard />
        <TeamCard />
        <TeamCard />
        <TeamCard />
        <div
          className={`${hovereff.normal} relative w-[370px] flex flex-col h-[460px]
          cursor-pointer rounded-[25px] rounded-tr-[85px] hover:rounded-tr-[25px] overflow-hidden mt-4 bg-[#4C6CE2] pl-8 pt-8 leading-[80px]`}
        >
          <p className="font-lt text-white text-[64px] max-w-[50%]">
            Meet the Entire Team
          </p>
          <Button
            size="lg"
            className="absolute bottom-0 left-0 rounded-none rounded-tr-[25px] rounded-bl-[24px] bg-[#4FC38F] text-white font-bld w-[165px]"
          >
            Explore
          </Button>
        </div>
      </div>
    </div>
  );
};

const Home = () => {
  const cards = [
    { name: "Policymaker", icn: Academic_icn },
    { name: "Farmer", icn: Farmer_icn },
    { name: "Academic", icn: Policymake_icn },
  ];
  const [isEnter, setIsEnter] = useState(false);

  return (
    <div className="w-screen flex flex-col  justify-start bg-[#F2F9F3]">
      <div className="w-full p-4 bg-[#F2F9F3] h-screen font-Myfont flex flex-col">
        <Header />
        <div className="relative w-full grow pt-2">
          <HeroSc />
        </div>
      </div>
      {/* <div className="w-full p-20 bg-[#ffffff] z-10"></div> */}

      <OurStory />
      <div className="w-full p-20 bg-[#ffffff] z-10"></div>
      <div className="w-full p-14 bg-[#F2F9F3] z-10"></div>
      <ProductSc />
      {/* <div className="w-full p-14 bg-[#ffffff] z-10"></div> */}
      <div className="w-full p-20 bg-[#F2F9F3] z-10"></div>
      <Team />
      <div className="w-full p-14 bg-[#ffffff] z-10"></div>
      <PartnersSc />
      <div className="w-full p-14 bg-[#ffffff] z-10"></div>
      <Contact />
      {/* <div className="w-full p-14 bg-[#ffffff] z-10"></div> */}
    </div>
  );
};

export default Home;
