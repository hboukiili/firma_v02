<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor xmlns="http://www.opengis.net/sld" version="1.0.0"
    xmlns:gml="http://www.opengis.net/gml"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:sld="http://www.opengis.net/sld">
  <UserLayer>
    <sld:LayerFeatureConstraints>
      <sld:FeatureTypeConstraint />
    </sld:LayerFeatureConstraints>
    <sld:UserStyle>
      <sld:Name>Ultra Fine Gradient</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="ramp">
              <sld:ColorMapEntry quantity="0.00" color="#d7191c" label="Very Low" />
              <sld:ColorMapEntry quantity="0.05" color="#e55626" />
              <sld:ColorMapEntry quantity="0.10" color="#e76429" />
              <sld:ColorMapEntry quantity="0.15" color="#f28732" />
              <sld:ColorMapEntry quantity="0.20" color="#f29c34" />
              <sld:ColorMapEntry quantity="0.25" color="#f2b435" />
              <sld:ColorMapEntry quantity="0.30" color="#f2db0c" label="Moderate" />
              <sld:ColorMapEntry quantity="0.35" color="#d4e80b" />
              <sld:ColorMapEntry quantity="0.40" color="#b6db0c" />
              <sld:ColorMapEntry quantity="0.45" color="#9ace0c" />
              <sld:ColorMapEntry quantity="0.50" color="#7fd90c" />
              <sld:ColorMapEntry quantity="0.55" color="#6cd40c" />
              <sld:ColorMapEntry quantity="0.60" color="#45f20c" />
              <sld:ColorMapEntry quantity="0.65" color="#3bc70c" />
              <sld:ColorMapEntry quantity="0.70" color="#2ebf0c" />
              <sld:ColorMapEntry quantity="0.75" color="#24b10c" />
              <sld:ColorMapEntry quantity="0.80" color="#19a40c" />
              <sld:ColorMapEntry quantity="0.85" color="#14910c" />
              <sld:ColorMapEntry quantity="0.90" color="#0e8a0c" />
              <sld:ColorMapEntry quantity="0.95" color="#0a740c" />
              <sld:ColorMapEntry quantity="1.00" color="#0a640c" label="High" />
            </sld:ColorMap>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </UserLayer>
</StyledLayerDescriptor>