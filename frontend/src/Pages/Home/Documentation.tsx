import Header from "../Components/Header";
import docBg from "../../assets/docBg.jpg";
import { Button, Card, CardBody, CardFooter, Image } from "@nextui-org/react";

export const HeroSc = ({ img, title, subTitlr }) => {
  return (
    <div className="font-Myfont relative overflow-hidden rounded-[30px] rounded-br-[200px]">
      <div className="absolute w-full flex flex-col justify-center mt-[10%] items-center">
        <p className="text-white font-bld text-[190px] leading-[90%]">
          {title}
        </p>
        <p className="text-white text-[24px]">{subTitlr}</p>
      </div>
      <img className="w-full" src={img} alt="" />
    </div>
  );
};

const ArticleCard = () => {
  return (
    <Card
      shadow="sm"
      //   key={index}
      isPressable
      onPress={() => console.log("item pressed")}
      className="w-[550px] font-Myfont h-[300px] pb-4"
    >
      <CardBody className="overflow-visible p-0 gap-4">
        <Image
          //   shadow="sm"
          radius="lg"
          //   height={"60%"}
          width="100%"
          //   alt={item.title}
          className="w-full object-cover h-[140px]"
          src={docBg}
        />
        <b className="font-bld pl-10 text-[38px]">Article</b>
      </CardBody>
      <CardFooter className="text-small justify-between p-10">
        <p className="text-left text-[16px] max-w-[260px]">
          Detailed information about the APIs used in our application.
        </p>
        <p className="text-black  rounded-full cursor-pointer font-md underline decoration-solid">
          Read More
        </p>
      </CardFooter>
    </Card>
  );
};

const Documentation = () => {
  const content = [
    {
      title: "Article",
      dis: "Understand the various models used in our application to simulate and analyze agricultural practices.",
    },
    {
      title: "Models",
      dis: "Understand the various models used in our application to simulate and analyze agricultural practices.",
    },
    {
      title: "APIs",
      dis: "Detailed information about the APIs used in our application.",
    },
  ];

  return (
    <div className="w-full p-4 bg-[#F2F9F3] font-Myfont flex flex-col gap-">
      <div className="flex flex-col gap-2 ">
        <Header />
        <HeroSc
          img={docBg}
          title={"Documentation"}
          subTitlr={
            "Your guide to understanding and utilizing our platform effectively."
          }
        />
      </div>
      <div  className="w-full  p-16 flex flex-col gap-20">
        {content.map((v, key) => {
          return (
            <div className="flex flex-col gap-8">
              <div className="flex flex-col ">
                <b className="font-bld pl-4 text-[38px] -ml-3">{v.title}</b>
                <p className="text-[16px] font-nrml">{v.dis}</p>
              </div>
              <div className="flex justify-between">
                <ArticleCard />
                <ArticleCard />
                <ArticleCard />
              </div>
              <p className="cursor-pointer font-md underline decoration-solid ">
                View All
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Documentation;
