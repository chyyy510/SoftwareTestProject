<template>
  <div class="theme-toggle">
    <label
      v-for="theme in themeOptions"
      :key="theme.value"
      class="theme-option"
    >
      <input type="radio" :value="theme.value" v-model="selectedTheme" />
      <span>{{ theme.label }}</span>
    </label>
  </div>
  <div ref="editorContainer" class="editor"></div>
</template>

<script>
import { onMounted, ref, watch } from "vue";
import ace from "ace-builds";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-monokai";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/theme-solarized_light";

export default {
  name: "AceEditor",
  props: {
    modelValue: String, // v-model 双向绑定
  },
  emits: ["update:modelValue"],
  setup(props, { emit }) {
    const editorContainer = ref(null);
    const selectedTheme = ref("monokai");
    //const selectedTheme = ref(props.theme);
    const themeOptions = [
      { value: "monokai", label: "Monokai" },
      { value: "github", label: "GitHub" },
      { value: "solarized_light", label: "Solarized" },
    ];

    let editor = null;

    onMounted(() => {
      editor = ace.edit(editorContainer.value);
      editor.setTheme(`ace/theme/${selectedTheme.value}`);
      editor.session.setMode("ace/mode/python");
      editor.setOptions({
        fontSize: "16px",
        showPrintMargin: false,
        highlightActiveLine: true,
        wrap: true,
      });

      editor.setValue(props.modelValue || "", 1); // 1 = 光标定位到末尾

      editor.session.on("change", () => {
        const newCode = editor.getValue();
        emit("update:modelValue", newCode);
      });
    });

    watch(selectedTheme, (newTheme) => {
      if (editor) {
        editor.setTheme(`ace/theme/${newTheme}`);
      }
    });

    return {
      editorContainer,
      selectedTheme,
      themeOptions,
    };
  },
};
</script>

<style scoped>
.editor {
  width: 800px;
  height: 600px;
  border: 1px solid #ddd;
}
.theme-toggle {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px;
}

.theme-option {
  position: relative;
  padding: 6px 12px;
  border-radius: 20px;
  background-color: #eee;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s;
}

.theme-option input[type="radio"] {
  display: none;
}

.theme-option input[type="radio"]:checked + span {
  background-color: #7dc05e;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
}
</style>
