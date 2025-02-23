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
      <sld:Name>Ultra Fine Gradient 0-100 (Interval 10)</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="ramp">
              <sld:ColorMapEntry quantity="0" color="#d7191c" label="Very Low" />
              <sld:ColorMapEntry quantity="10" color="#e76429" />
              <sld:ColorMapEntry quantity="20" color="#f29c34" />
              <sld:ColorMapEntry quantity="30" color="#f2db0c" label="Moderate" />
              <sld:ColorMapEntry quantity="40" color="#b6db0c" />
              <sld:ColorMapEntry quantity="50" color="#7fd90c" />
              <sld:ColorMapEntry quantity="60" color="#45f20c" />
              <sld:ColorMapEntry quantity="70" color="#2ebf0c" />
              <sld:ColorMapEntry quantity="80" color="#19a40c" />
              <sld:ColorMapEntry quantity="90" color="#0e8a0c" />
              <sld:ColorMapEntry quantity="100" color="#0a640c" label="High" />
            </sld:ColorMap>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </UserLayer>
</StyledLayerDescriptor>