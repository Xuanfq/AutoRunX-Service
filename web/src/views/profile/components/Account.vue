<template>
  <el-form disabled>
    <el-form-item label="Name">
      <el-input v-model.trim="user.name" />
    </el-form-item>
    <el-form-item label="Email">
      <el-input v-model.trim="user.email" />
    </el-form-item>
    <el-form-item label="Roles">
      <el-input :value="user.roles.join(' | ')" readonly />
    </el-form-item>
    <el-form-item label="Manager">
      <el-switch v-model="user.is_staff" />
    </el-form-item>
    <el-form-item label="Active">
      <el-switch v-model="user.is_active" />
    </el-form-item>
    <el-form-item label="Superuser">
      <el-switch v-model="user.is_superuser" />
    </el-form-item>
    <el-form-item v-if="user.date_joined && user.date_joined!='' && user.date_joined!=null" label="Create Time">
      <el-date-picker v-model="user.date_joined" type="datetime" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit" :disabled="true">Update</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: '',
          email: '',
          roles: [],
          avatar: '',
          is_staff: false,
          is_active: false,
          is_superuser: false,
          date_joined: '',
        }
      }
    }
  },
  methods: {
    submit() {
      this.$message({
        message: 'Block',
        type: 'success',
        duration: 5 * 1000
      })
    }
  }
}
</script>
