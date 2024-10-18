import Bouregreg_ from "../../assets/Watershed/SvgSubCoordinates/Bouregreg/Bouregreg_"
import Chaouia from "../../assets/Watershed/SvgSubCoordinates/Bouregreg/Chaouia"
import CtAtlantiques from "../../assets/Watershed/SvgSubCoordinates/Bouregreg/Côtiers atlantiques"
import HautDaraa from "../../assets/Watershed/SvgSubCoordinates/Daraa/HautDaraa"
import BasDaraa from "../../assets/Watershed/SvgSubCoordinates/Daraa/BasDaraa"
import GuirBouanane from "../../assets/Watershed/SvgSubCoordinates/Guir - Ziz - Rhris/Guir - Bouanane"
import ZizRheris from "../../assets/Watershed/SvgSubCoordinates/Guir - Ziz - Rhris/Ziz-Rheris"
import Zouzfana from "../../assets/Watershed/SvgSubCoordinates/Moulouya/Zouzfana (unité de Figuig)"
import Isly from "../../assets/Watershed/SvgSubCoordinates/Moulouya/Isly"
import Nador from "../../assets/Watershed/SvgSubCoordinates/Moulouya/Nador (Kert)"
import Moulouya_ from "../../assets/Watershed/SvgSubCoordinates/Moulouya/Moulouya_"
import cotierEssaouira from "../../assets/Watershed/SvgSubCoordinates/Tensift/Cotier Essaouira"
import tensift_ from "../../assets/Watershed/SvgSubCoordinates/Tensift/tensift_r"
import TiznitIfni from "../../assets/Watershed/SvgSubCoordinates/Souss Massa/Tiznit - Ifni"
import Massa from "../../assets/Watershed/SvgSubCoordinates/Souss Massa/Massa"
import Tamri from "../../assets/Watershed/SvgSubCoordinates/Souss Massa/Tamri"
import Souss from "../../assets/Watershed/SvgSubCoordinates/Souss Massa/Souss"


export interface Weather {
    Rh: number,
    Rs: number,
    Ta: number,
    Ws: number,
    date: string,
}

export interface Weather_ {
    type: string,
    dates: string[],
    values: number[],
    url: string[],
    Bassin: string,
}

export interface SurfaceVariable {
    type: string,
    dates: string[],
    values: number[],
    url: string[],
    Bassin: string,
}

type SubWatershedType = {
    [key: string]: {
        item: { name: string; d: string }[];
    };
};


export const initialSubW: SubWatershedType = {
    "Bouregreg": {
        item: [
            { name: "Bouregreg", d: Bouregreg_ },
            { name: "Chaouia", d: Chaouia },
            { name: "Côtiers atlantiques", d: CtAtlantiques },
        ]
    },
    "Daraa": {
        item: [
            { name: "Haut Daraa", d: HautDaraa },
            { name: "Bas Daraa", d: BasDaraa },
        ]
    },
    "Guir - Ziz - Rhris": {
        item: [
            { name: "Guir - Bouanane", d: GuirBouanane },
            { name: "Ziz - Rheris", d: ZizRheris },
        ]
    },
    "Moulouya": {
        item: [
            { name: "Zouzfana (unité de Figuig)", d: Zouzfana },
            { name: "Isly", d: Isly },
            { name: "Nador (Kert)", d: Nador },
            { name: "Moulouya", d: Moulouya_ },
        ]
    },
    "Tensift": {
        item: [
            { name: "Cotier Essaouira", d: cotierEssaouira },
            { name: "Tensift", d: tensift_ },
        ]
    },
    "Souss Massa": {
        item: [
            { name: "Tiznit - Ifni", d: TiznitIfni },
            { name: "Massa", d: Massa },
            { name: "Tamri", d: Tamri },
            { name: "Souss", d: Souss },
        ]
    },
    // "Oum Er Rbia": {
    // },
    // "Loukkous": {
    // },
    // "Sahara": {
    // },
    // "Sebou": {
    // },
}

export interface policyMaker {
    isLoading: boolean,
    isSubmit: boolean,
    IsBaseMap: boolean,
    IsGeoRaster: boolean,
    IsAllDataReceived: boolean,
    WatershedId: string,
    SubWatershedId: string,
    Imgs: string[],
    SubWatersheds: typeof initialSubW,
    StartDate: string,
    EndDate: string,
    Band: string,
    loadingMsg: string,
    Dates: Date[],
    ChartData: Weather_ | null,
    Weather: Weather_[],
    SurfaceVariable: SurfaceVariable[],
    Flux: SurfaceVariable[],
}