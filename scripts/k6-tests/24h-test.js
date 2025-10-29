import http from 'k6/http';
import { check, sleep } from 'k6';

function randomCoordInCircle(centerLat, centerLon, radiusMeters) {
    const radiusInDegrees = radiusMeters / 111320; // ~111.32 km por grau de latitude

    const angle = Math.random() * 2 * Math.PI;
    const distance = Math.sqrt(Math.random()) * radiusInDegrees;

    const deltaLat = distance * Math.cos(angle);
    const deltaLon = distance * Math.sin(angle) / Math.cos(centerLat * Math.PI / 180); // corrige para longitude

    return [centerLon + deltaLon, centerLat + deltaLat]; // [lon, lat] (formato GeoJSON)
}


export const options = {

};

/*

    scenarios: {
        high_throughput: {
        executor: 'contant-arrival-rate',
        duration: '1h',
        rate: 1000, 
        timeUnit: '1s', 
        preAllocatedVUs: 250,

        },
    },

// Called once before all VUs start
export function setup() {
    const url = 'http://192.168.0.95:31357/ngsi-ld/v1/entities';
    const headers = {
        headers: {
            'Content-Type': 'application/ld+json'
        }
    };

    // Create one entity per VU
    let entityIds = [];
    
    const centerLat = -20.27868363298307;
    const centerLon = -40.29781714837235;
    const radius = 1000; // 1 km

    for (let i = 1; i <= options.vus; i++) {
        const entityId = `urn:ngsi-ld:ArtificialSensor:${i}`;
        const [lon, lat] = randomCoordInCircle(centerLat, centerLon, radius);
        const entity = {
            id: entityId,
            type: "ArtificialSensor",
            name: {
                type: "Property",
                value: `Artificial Sensor ${i}`
            },
            peopleCount: {
                type: "Property",
                value: 0
            },
            location: {
                type: "GeoProperty",
                value: {
                    type: "Point",
                    coordinates: [lon, lat] // [lon, lat] (formato GeoJSON)
                }
            },
            timestamp: {
                type: "Property",
                value: new Date().toISOString()
            },
            "@context": [
                "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context-v1.8.jsonld",
                "https://fiware.github.io/data-models/context.jsonld"
            ]
        };

        const res = http.post(url, JSON.stringify(entity), headers);

        check(res, {
            [`created or exists sensor ${i}`]: (r) => r.status === 201 || r.status === 409
        });

        entityIds.push(entityId);
    }

    return { entityIds };
}
*/


// Called by each VU on each iteration
export default function (data) {
    const entityId = `urn:ngsi-ld:ArtificialSensor:${__VU}`; // __VU starts at 1
    const updateUrl = `http://192.168.0.95:31357/ngsi-ld/v1/entities/${entityId}/attrs/peopleCount`;

    const updateHeaders = {
        headers: {
            'Content-Type': 'application/json',
            'Link': '<https://fiware.github.io/data-models/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
            'Accept': 'application/json'
        }
    };

    const newValue = Math.floor(Math.random()*100);
    const updateBody = JSON.stringify({
        type: "Property",
        value: newValue
    });

    const res = http.patch(updateUrl, updateBody, updateHeaders);

    check(res, {
        [`VU ${__VU} update OK`]: (r) => r.status === 204
    });
}
