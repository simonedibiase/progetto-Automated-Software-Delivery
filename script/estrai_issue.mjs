import { Octokit } from "@octokit/core";
import fs from "fs";

const octokit = new Octokit({
    auth: '' //inserire il proprio token
});

async function getAllIssues() {
    let allIssuesData = [];
    let page = 1;
    const perPage = 100;

    try {
        while (true) {
            console.log(`Recupero della pagina ${page}...`);

            const response = await octokit.request('GET /repos/{owner}/{repo}/issues', {
                owner: 'vuejs',
                repo: 'vue',
                headers: {
                    'X-GitHub-Api-Version': '2022-11-28'
                },
                per_page: perPage,
                page: page,
                state: 'all' 
            });

            const issues = response.data;

            for (const issue of issues) {
                if (issue.pull_request) continue;

                if (issue.labels.some(label => label.name === 'bug')) {
                    allIssuesData.push({
                        number: issue.number,
                        title: issue.title,
                        labels: issue.labels.map(label => label.name),
                        assignee: issue.assignee ? issue.assignee.login : null,
                        state: issue.state
                    });
                    console.log(`Analizzata issue #${issue.number} con tag 'bug'`);
                }
            }

            if (issues.length < perPage) break;

            page++;

        }

        fs.writeFileSync('filtered_bug_issues.json', JSON.stringify(allIssuesData, null, 2), 'utf-8');
        console.log("Tutte le issue con il tag 'bug' sono state salvate in filtered_bug_issues.json");

    } catch (error) {
        console.error("Errore durante la richiesta:", error);
    }
}

getAllIssues();
