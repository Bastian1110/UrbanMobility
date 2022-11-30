using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;


    public AgentData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
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
    string initEndpoint = "/init";
    string updateEndpoint = "/update";

    AgentsData carsData;
    Dictionary<string, GameObject> agents;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, started = false;

    public GameObject carPrefab, floor;
    public int NCars, width, height;
    public float timeToUpdate = 0.1f;
    private float timer, dt;

    // Start is called before the first frame update
    void Start()
    {
        carsData = new AgentsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();

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
                Vector3 newAgentPosition = new Vector3(agent.x + 0.9f, agent.y - 0.95f, agent.z + 0.15f);

                if (!started)
                {
                    prevPositions[agent.id] = newAgentPosition;
                    agents[agent.id] = Instantiate(carPrefab, newAgentPosition, Quaternion.identity);
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
        updated = true;
        if (!started) started = true;
    }
}