using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;
    public bool state;


    public AgentData(string id, float x, float y, float z, bool state)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.state = state;
    }
}

[Serializable]
public class AgentsData
{
    public List<AgentData> positions;
    public AgentsData() => this.positions = new List<AgentData>();
}

public class GameController : MonoBehaviour
{
    public string serverUrl = "http://localhost:8080";
    string getCarsEndpoint = "/getCars";
    string getTLEndpoint = "/getTrafficLights";
    string initEndpoint = "/init";
    string updateEndpoint = "/update";

    public List<GameObject> carsPrefabs;
    private int randomIndex;

    AgentsData carsData;
    AgentsData tlData;
    Dictionary<string, GameObject> agents, tlAgents;
    Dictionary<string, Vector3> prevPositions, currPositions;
    Dictionary<string, bool> currTLState; 

    bool updated = false, started = false;

    public GameObject tlPrefab, floor;


    public int NCars, width, height;
    public float timeToUpdate = 0.1f;
    private float timer, dt;

    // Start is called before the first frame update
    void Start()
    {
        carsData = new AgentsData();
        tlData = new AgentsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        currTLState = new Dictionary<string, bool>();

        agents = new Dictionary<string, GameObject>();
        tlAgents = new Dictionary<string, GameObject>();

        floor.transform.localScale = new Vector3((float)width / 10, 1, (float)height / 10);
        floor.transform.localPosition = new Vector3((float)width / 2 - 0.5f, 1, (float)height / 2 - 0.5f);

        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }


    // Update is called once per frame
    void Update()
    {
        if (timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach (var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if (direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
            }

            foreach (var agent in currTLState)
            {
                if(agent.Value == false)
                {
                    tlAgents[agent.Key].GetComponent<Renderer>().materials[0].color = Color.red;
                }
                else
                {
                    tlAgents[agent.Key].GetComponent<Renderer>().materials[0].color = Color.green;
                }
            }
        }
    }

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            StartCoroutine(GetCarsData());
            StartCoroutine(GetTLData());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NCars", NCars.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + initEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetCarsData());
            StartCoroutine(GetTLData());
        }
    }

    IEnumerator GetCarsData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCarsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            carsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach (AgentData agent in carsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y - 0.95f, agent.z);
                if (!started)
                {
                    prevPositions[agent.id] = newAgentPosition;
                    randomIndex = UnityEngine.Random.Range(0, carsPrefabs.Count());
                    agents[agent.id] = Instantiate(carsPrefabs[randomIndex], newAgentPosition, Quaternion.identity);
                }
                else
                {
                    if(agent.state == false)
                    {
                        Destroy(agents[agent.id]);
                        prevPositions.Remove(agent.id);
                        currPositions.Remove(agent.id);
                        agents.Remove(agent.id);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if (currPositions.TryGetValue(agent.id, out currentPosition))
                            prevPositions[agent.id] = currentPosition;
                        currPositions[agent.id] = newAgentPosition;
                    }
                }
            }
        }
    }

    IEnumerator GetTLData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTLEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            tlData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach (AgentData agent in tlData.positions)
            {
                if (!started)
                {
                    Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                    currTLState[agent.id] = agent.state;
                    tlAgents[agent.id] = Instantiate(tlPrefab, newAgentPosition, Quaternion.identity);
                }
                else
                {
                    currTLState[agent.id] = agent.state;
                }
            }
        }
        updated = true;
        if (!started) started = true;
    }
}