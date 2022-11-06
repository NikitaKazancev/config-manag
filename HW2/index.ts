import { IFetchResponse } from './IFetchResponse';

import https from 'node:https';

const createOutputGraph = (packageName: string, dependencies: string[]) => {
   const createNode = (dependency: string, i: number) => {
      return `"node${i}" [\nlabel = "${dependency}"\n];\n`;
   };

   const createDependency = (parent: string, child: string, id: number) => {
      return `"${parent}" -> "${child}" [\nid = ${id}\n];\n`;
   };

   let output = 'digraph Dependencies {\n';
   output += createNode(packageName, 0);

   dependencies.forEach((dependency, i) => {
      output += createNode(dependency, i + 1);
   });

   dependencies.forEach((dependency, i) => {
      output += createDependency(packageName, dependency, i);
   });

   output += '}';
   return output;
};

const main = (): void => {
   if (process.argv.length < 3) return;

   const packageName = process.argv[2];
   const url = `https://pypi.org/pypi/${packageName}/json`;

   https.get(url, req => {
      const chunks: any = [];
      req.on('data', data => {
         chunks.push(data);
      });

      req.on('end', () => {
         const data: IFetchResponse = JSON.parse(
            Buffer.concat(chunks).toString()
         );

         if (!data['info']) {
            return console.log(`No info about package '${packageName}'`);
         }

         if (!data['info']['requires_dist']) {
            return console.log('There is no dependencies :)');
         }

         const dependencies: string[] = data['info']['requires_dist'];
         console.log(createOutputGraph(packageName, dependencies));
      });

      req.on('error', () => {
         console.log(`Could not fetch ${url}`);
      });
   });
};

main();
