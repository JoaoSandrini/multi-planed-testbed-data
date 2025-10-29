import http from 'k6/http';
import { check, sleep } from 'k6';
import exec from 'k6/x/exec';

export const options = {
    scenarios: {
        slowRoute:{
            exec: 'make_requests',
            executor: 'contant-arrival-rate',
            duration: '10m',
            preAllocatedVUs: 15,
            maximumVUs: 20,
            timeUnit: '1s',
            rate: '110', 
        },
        swapRoute: {
            exec: 'swap_route',
            iterations: 1,
        },
        fastRoute: {
            exec: 'make_requests',
            executor: 'contant-arrival-rate',
            duration: '50m',
            preAllocatedVUs: 15,
            maximumVUs: 20,
            timeUnit: '1s',
            rate: '110', 
        },
    }
};

export function make_requests () {
    const entityId = `urn:ngsi-ld:ArtificialSensor:${__VU}`; // __VU starts at 1
    const updateUrl = `http://200.137.66.110:31881/ngsi-ld/v1/entities/${entityId}/attrs/peopleCount`;

    const updateHeaders = {
        headers: {
            'Content-Type': 'application/json',
            'Link': '<https://fiware.github.io/data-models/context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
            'Accept': 'application/json'
        }
    };

    const newValue = Math.floor(Math.random()*10);
    const updateBody = JSON.stringify({
        type: "Property",
        value: newValue
    });

    const res = http.patch(updateUrl, updateBody, updateHeaders);

    check(res, {
        [`VU ${__VU} update OK`]: (r) => r.status === 204
    });
}

export function swap_route () {
    exec.command('python3.6 /home/everson/change-to-rj.py');
}    