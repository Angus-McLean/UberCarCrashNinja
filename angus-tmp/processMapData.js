XML_STR = `

`;
var xmlObj = xmlToJSON.parseString(XML_STR);

// print all relation attributes types
_.flattenDeep(_.map(xmlObj.osm[0].relation, item => _.map(item.tag, '_attr.k._value')))

/* The Extraction Plan Weeeeep
- filter for ways that their tags contain "highway"

*/

// get all 'way''s that contain highways
var waysTypeHighWay = _.filter(xmlObj.osm[0].way, way => {
  return _.map(way.tag, '_attr.k._value').includes('highway');
})

function getPropertyFromItem(item, prop) {
  return _.get(_.find(item.tag, {_attr:{k:{_value: prop}}}), '_attr.v._value')
}

function fetchNodeById(nodeId) {
  return _.find(xmlObj.osm[0].node, {_attr: {id : {_value: nodeId}}});
}

function simplifyNode(node) {
  return _.pluck(node, )
}

var ROADS = _.map(waysTypeHighWay, road => {
	var roadObj = {
		id : _.get(road, '_attr.id._value'),
		uid : _.get(road, '_attr.uid._value'),
		name : getPropertyFromItem(road, 'name')
  };

  roadObj.nodes = _.map(road.nd, "_attr.ref._value").map(fetchNodeById).map(function (node) {
    return {
      id : node._attr.id._value,
      lat : node._attr.lat._value,
      lon : node._attr.lon._value
    };
  })
  return roadObj;
});
