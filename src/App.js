import TheContent from "./components/TheContent.js";
import TheFooter from "./components/TheFooter.js";
import TheHeader from "./components/TheHeader.js";
import Repository from "./data/repository.js";

import "./css/theme.css"

function App() {

	const repository = new Repository()

	return (
		<div>
			<TheHeader />
			<div id="container">
				<TheContent repo={repository} />
			</div>
			<TheFooter />
		</div>
	);
}

export default App;
