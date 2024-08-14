import React from "react";
import { Carousel } from 'antd';
import Slide_bg from '../../../assets/slide.jpg'

const Slider_ = () => {

  const contentStyle: React.CSSProperties = {
    height: '340px',
    width: '100%',
    color: '#fff',
    lineHeight: '160px',
    textAlign: 'center',
    background: '#364d79',
    // borderRadius: '15px 0px 0px 15px'
  };
  return (

    <Carousel className="rounded-tl-[15px] rounded-bl-[15px] overflow-hidden" autoplay>
      <div className="relative">
        <h1 className="absolute bottom-4 left-7 text-[40px] font-Myfont font-bld text-Lgreen">Unlocking Agricultural Success <br />
          through Research and Insights</h1>
        <img src={Slide_bg} style={contentStyle} />
      </div>
      <div className="relative">
        <h1 className="absolute bottom-4 left-7 text-[40px] font-Myfont font-bld text-Lgreen">Unlocking Agricultural Success <br />
          through Research and Insights</h1>
        <img src={Slide_bg} style={contentStyle} />
      </div>
      <div className="relative">
        <h1 className="absolute bottom-4 left-7 text-[40px] font-Myfont font-bld text-Lgreen">Unlocking Agricultural Success <br />
          through Research and Insights</h1>
        <img src={Slide_bg} style={contentStyle} />
      </div>


    </Carousel>
  )
}

export default Slider_