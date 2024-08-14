import React, { useEffect, useState } from "react";
import api from "../../../api/axios.js"
import SelectField from "./SelectField.js";
import Humidity_icon from "../../../assets/humidity.svg"
import Speed_icon from "../../../assets/speed.svg"
import Pressure_icon from "../../../assets/Pressure.svg"
import { ReactSVG } from "react-svg";

interface Field_ {
  [key: string]: any
}

interface Location {
  latitude: number;
  longitude: number;
}

const WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5';
const WEATHER_API_KEY = 'bfc01f870ae21dc5c8b4eb1f2c0eadba';
const WEATHER_ICON_URL = 'https://openweathermap.org/img/wn/';
const WEATHER_ICON_EXT = '@2x.png';

const DateFormatter = ({ dateString }) => {
  const dateObject = new Date(dateString);
  const options = { weekday: 'long' };
  const dayOfWeek = dateObject.toLocaleDateString('en-US', options);

  return <span className="font-Myfont font-smbld text-[14px]">{dayOfWeek}</span>;
};

export async function fetchWeatherData(lat, lon) {
  try {
    let [weatherPromise, forcastPromise] = await Promise.all([
      fetch(
        `${WEATHER_API_URL}/weather?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`
      ),
      fetch(
        `${WEATHER_API_URL}/forecast?lat=${lat}&lon=${lon}&appid=${WEATHER_API_KEY}&units=metric`
      ),
    ]);

    const weatherResponse = await weatherPromise.json();
    const forcastResponse = await forcastPromise.json();
    return [weatherResponse, forcastResponse];
  } catch (error) {
    console.log(error);
  }
}
const Weather = (Name) => {

  const [selectedField, setSelectedField] = useState<Field_>();
  const [fields, setFields] = useState<Field_>([]);
  const [loading, setLoading] = useState(true);
  const [weatherData, setWeatherData] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [submitted, setSubmitted] = useState(false);
  const [selectedOption, setSelectedOption] = useState('');
  const [location, setLocation] = useState<Location | null>(null);
  const mapRef = React.useRef();
  console.log(Name,"99999")
  // Fetch the fields data from the Django API endpoint
  async function fetch() {
    await api.get('/api/field/')
      .then(response => {
        setFields(response.data);
        setSelectedField(response.data[Name.Name])
      })
      .catch(error => {
        console.log(error);
      });
  }

  const handleMapClick = event => {
    const { latlng } = event;
    const { lng, lat } = latlng;

    // Find the field that contains the clicked point
    const clickedField = fields.find(field => {
      const boundaries = JSON.parse(field.boundaries);
      return isPointInPolygon([lng, lat], boundaries);
    });

    if (clickedField) {
      setSelectedField(clickedField);
      setSelectedOption(clickedField.field_id); // Update the selected option in the dropdown
    }
  };

  const handleSelectChange = event => {
    const selectedFieldId = event.target.value;
    const field = fields.find(field => field.field_id == selectedFieldId);
    setSelectedField(field);
    setSelectedOption(selectedFieldId);
    flyToField(field);
  };

  const isPointInPolygon = (point, polygon) => {
    const x = point[0];
    const y = point[1];
    let isInside = false;

    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
      const xi = polygon[i][0];
      const yi = polygon[i][1];
      const xj = polygon[j][0];
      const yj = polygon[j][1];

      const intersect =
        yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi;
      if (intersect) {
        isInside = !isInside;
      }
    }

    return isInside;
  };

  const calculateCentroid = coords => {
    const n = coords.length;
    let sumX = 0;
    let sumY = 0;

    for (let i = 0; i < n; i++) {
      const [x, y] = coords[i];
      sumX += x;
      sumY += y;
    }

    const centroidX = sumX / n;
    const centroidY = sumY / n;

    return [centroidX, centroidY];
  };

  const handleSubmit = async () => {
    setSubmitted(true);
    if (selectedField?.boundaries) {
      const boundaries = JSON.parse(selectedField?.boundaries);
      const centroid = calculateCentroid(boundaries);
      const [lon, lat] = centroid;
      fetchWeatherData(lat, lon)
        .then(([weatherResponse, forecastResponse]) => {
          setWeatherData(weatherResponse);
          setForecastData(forecastResponse.list.filter((_, index) => index % 8 === 0));
          setLoading(false);
        })
        .catch(error => {
          console.log(error);
        });
    }
    else {
      navigator.geolocation.getCurrentPosition(
        function (position) {
          console.log("wobi")
          const { latitude, longitude } = position.coords;
          setLocation({ latitude, longitude });
        },
        function (error) {
          console.error("Error getting geolocation:", error);
        }
      );
      
      fetchWeatherData(location?.latitude, location?.longitude)
        .then(([weatherResponse, forecastResponse]) => {
          console.log("wobi")
          setWeatherData(weatherResponse);
          setForecastData(forecastResponse);
          setLoading(false);
        })
        .catch(error => {
          console.log("wobi")
          console.log(error);
        });
    }
  };

  const flyToField = (field) => {
    if (mapRef.current) {
      const boundaries = JSON.parse(field.boundaries);
      const bounds = boundaries.map((coord) => [coord[1], coord[0]]);
      mapRef.current.flyToBounds(bounds);
    }
  };

  useEffect(() => {
    fetch()
    handleSubmit()
  }, [Name])
  
  if (!weatherData || !forecastData.length) {
    console.log(weatherData, forecastData, selectedField)
    return (<div ></div>)
  }
  return (
    <div className="w-full flex flex-col gap-[1rem] md:flex-row ">
      <div className="w-full flex justify-center items-center md:w-[46%] h-[9rem]">
        <div className="bg-[#EAF3E9] h-full w-full rounded-[1.5rem] flex items-center gap-1 justify-evenly relative">
          <div className="flex flex-col h-[80%] max-w-[35%]">
            <h1 className="font-Myfont font-bld text-[18px] text-black">Today</h1>
            <h1 className="font-Myfont font-nrml text-[18px] text-black">
              {weatherData.weather[0].description}
            </h1>
          </div>
          <div className="max-w-[35%] flex flex-col justify-center items-center">
            <img className=" w-full drop-shadow-lg" src={WEATHER_ICON_URL + weatherData.weather[0].icon + WEATHER_ICON_EXT} alt='icon' />
            <h1 className="font-Myfont text-DarkGreen text-[18px] font-bld">{weatherData.main.temp} C°</h1>
          </div>
          <div className="flex flex-col h-[70%] justify-evenly">
            <div className="flex text-black font-Myfont font-md text-[14px]  justify-start gap-2 items-center w-[100%] ">
              <ReactSVG src={Speed_icon} />
              {weatherData.wind.speed} m/s
            </div>
            <div className="flex text-black font-Myfont font-md text-[14px]  justify-start gap-2 items-center w-[100%] ">
              <ReactSVG src={Humidity_icon} />
              {weatherData.main.humidity} %
            </div>
            <div className="flex  text-black font-Myfont font-md text-[14px]  justify-start gap-2 items-center w-[100%] ">
              <ReactSVG src={Pressure_icon} />
              {weatherData.main.pressure} hPa
            </div>
          </div>
        </div>
      </div>
      <div className="w-full flex gap-[1rem] flex-col md:flex-row md:justify-between">
        <div className="h-[9rem] flex justify-between items-center md:w-[48%] ">
          <div className="bg-[#EAF3E9] w-[48%] h-full 0 rounded-[1.5rem]   flex flex-col justify-between items-center">
            <div className="flex flex-col items-center w-[100%] max-w-[100%] text-black">
              <DateFormatter dateString={forecastData[1].dt_txt} />
              <div className="overflow-hidden w-[100%] h-[4rem] flex justify-center items-center">
                <img className="drop-shadow-lg w-[50%] top-[-10px]" src={WEATHER_ICON_URL + forecastData[1].weather[0].icon + WEATHER_ICON_EXT} alt='icon' />
              </div>
            </div>
            <div className="flex justify-between items-center w-[90%] max-w-[90%] text-black">
              <div className="flex font-Myfont font-md text-[14px]  justify-between gap-2 items-center w-[50%] ">
                <ReactSVG src={Speed_icon} />
                {forecastData[1].wind.speed} m/s
              </div>
              <div className="flex font-Myfont  font-md text-[14px]  justify-between gap-2 items-center w-[35%] ">
                <ReactSVG src={Humidity_icon} />
                {forecastData[1].main.humidity} %
              </div>
            </div>
            <h1 className="font-Myfont font-nrml text-[14px] text-black">
              {forecastData[1].weather[0].description}
            </h1>
          </div>
          <div className="bg-[#EAF3E9] w-[48%] h-full text-black  rounded-[1.5rem]   flex flex-col justify-between items-center">
            <div className="flex flex-col items-center w-[100%] max-w-[100%]">
              <DateFormatter dateString={forecastData[2].dt_txt} />
              <div className="overflow-hidden w-[100%] h-[4rem] flex justify-center items-center">
                <img className="drop-shadow-lg w-[50%] top-[-10px]" src={WEATHER_ICON_URL + forecastData[2].weather[0].icon + WEATHER_ICON_EXT} alt='icon' />
              </div>
            </div>
            <div className="flex justify-between   items-center w-[90%] max-w-[90%]">
              <div className="flex font-Myfont font-md text-[14px]  justify-between gap-2 items-center w-[50%] ">
                <ReactSVG src={Speed_icon} />
                {forecastData[2].wind.speed} m/s
              </div>
              <div className="flex font-Myfont font-md text-[14px]  justify-between gap-2 items-center w-[35%] ">
                <ReactSVG src={Humidity_icon} />
                {forecastData[2].main.humidity} %
              </div>
            </div>
            <h1 className="font-Myfont font-nrml text-[14px] ">
              {forecastData[2].weather[0].description}
            </h1>
          </div>
        </div>
        <div className="h-[9rem] flex justify-between items-center md:w-[48%] text-black">
        <div className="bg-[#EAF3E9] w-[48%] h-full  rounded-[1.5rem]   flex flex-col justify-between items-center">
            <div className="flex flex-col items-center w-[100%] max-w-[100%]">
              <DateFormatter dateString={forecastData[3].dt_txt} />
              <div className="overflow-hidden w-[100%] h-[4rem] flex justify-center items-center">
                <img className="drop-shadow-lg w-[50%] top-[-10px]" src={WEATHER_ICON_URL + forecastData[3].weather[0].icon + WEATHER_ICON_EXT} alt='icon' />
              </div>
            </div>
            <div className="flex justify-between items-center w-[90%] max-w-[90%]">
              <div className="flex font-Myfont font-md text-[14px]  justify-between gap-2 items-center w-[50%] ">
                <ReactSVG src={Speed_icon} />
                {forecastData[3].wind.speed} m/s
              </div>
              <div className="flex font-Myfont font-md text-[14px]  justify-between gap-2 items-center w-[35%] ">
                <ReactSVG src={Humidity_icon} />
                {forecastData[3].main.humidity} %
              </div>
            </div>
            <h1 className="font-Myfont font-nrml text-[14px] ">
              {forecastData[3].weather[0].description}
            </h1>
          </div>
          <div className="bg-[#EAF3E9] w-[48%] h-full b rounded-[1.5rem]   flex flex-col justify-between items-center">
            <div className="flex flex-col items-center w-[100%] max-w-[100%]">
              <DateFormatter dateString={forecastData[4].dt_txt} />
              <div className="overflow-hidden w-[100%] h-[4rem] flex justify-center items-center">
                <img className="drop-shadow-lg w-[50%] top-[-10px]" src={WEATHER_ICON_URL + forecastData[4].weather[0].icon + WEATHER_ICON_EXT} alt='icon' />
              </div>
            </div>
            <div className="flex justify-between items-center w-[90%] max-w-[90%]">
              <div className="flex font-Myfont font-md text-[14px]  justify-between gap-2 items-center w-[50%] ">
                <ReactSVG src={Speed_icon} />
                {forecastData[4].wind.speed} m/s
              </div>
              <div className="flex font-Myfont font-md text-[14px]  justify-between gap-2 items-center w-[35%] ">
                <ReactSVG src={Humidity_icon} />
                {forecastData[4].main.humidity} %
              </div>
            </div>
            <h1 className="font-Myfont font-nrml text-[14px] ">
              {forecastData[4].weather[0].description}
            </h1>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Weather